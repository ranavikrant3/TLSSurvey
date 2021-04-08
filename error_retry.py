import concurrent.futures
import sys
import redis
from sslyze import (
    ServerNetworkLocationViaDirectConnection,
    ServerConnectivityTester,
    Scanner,
    ServerScanRequest,
    ScanCommand,
)
from sslyze.errors import ConnectionToServerFailed
r=redis.Redis(host='127.0.0.1',port='6379')

def runsslyze(seq):
    hostname=r.hget(seq,"hostname")
    status=r.hget(seq,"STATUS")
    if str(status)!='1':
        scan_runner(seq,hostname)
    return


def scan_runner(seq,host):
    hostname=host.decode("utf-8")
    servers_to_scan = []
    server_location = None
    try:
        server_location = ServerNetworkLocationViaDirectConnection.with_ip_address_lookup(hostname, 443)
        r.hset(seq,"ipaddr",server_location.ip_address)
        #Initialize with hostname, port int and ip address str 
        #print(server_location)
    except Exception as e:
        print(e)
        r.hset(seq,"STATUS",2)
    try:
        server_info = ServerConnectivityTester().perform(server_location)
        servers_to_scan.append(server_info)
    except ConnectionToServerFailed as e:
        r.hset(seq,"STATUS",3)
        return

    scanner = Scanner()

    # Then queue some scan commands for each server
    for server_info in servers_to_scan:
        server_scan_req = ServerScanRequest(
            server_info=server_info, scan_commands={ScanCommand.TLS_1_3_CIPHER_SUITES,ScanCommand.TLS_1_2_CIPHER_SUITES,ScanCommand.TLS_1_1_CIPHER_SUITES,ScanCommand.TLS_1_0_CIPHER_SUITES},
        )
        scanner.queue_scan(server_scan_req)

    # Then retrieve the result of the scan commands for each server
    for server_scan_result in scanner.get_results():
        try:
            tls1_3_result = server_scan_result.scan_commands_results[ScanCommand.TLS_1_3_CIPHER_SUITES]
            cipherstr=""
            if tls1_3_result.accepted_cipher_suites:
                for accepted_cipher_suite in tls1_3_result.accepted_cipher_suites:
                    cipherstr=cipherstr+str(accepted_cipher_suite.cipher_suite.name)+" "
                r.hset(seq,"TLS1_3",cipherstr)

            tls1_2_result = server_scan_result.scan_commands_results[ScanCommand.TLS_1_2_CIPHER_SUITES]
            cipherstr=""
            if tls1_2_result.accepted_cipher_suites:
                for accepted_cipher_suite in tls1_2_result.accepted_cipher_suites:
                    cipherstr=cipherstr+str(accepted_cipher_suite.cipher_suite.name)+" "
                r.hset(seq,"TLS1_2",cipherstr)

            tls1_1_result = server_scan_result.scan_commands_results[ScanCommand.TLS_1_1_CIPHER_SUITES]
            cipherstr=""
            if tls1_1_result.accepted_cipher_suites:
                for accepted_cipher_suite in tls1_1_result.accepted_cipher_suites:
                    cipherstr=cipherstr+str(accepted_cipher_suite.cipher_suite.name)+" "
                r.hset(seq,"TLS1_1",cipherstr)

            tls1_0_result = server_scan_result.scan_commands_results[ScanCommand.TLS_1_0_CIPHER_SUITES]
            cipherstr=""
            if tls1_0_result.accepted_cipher_suites:
                for accepted_cipher_suite in tls1_0_result.accepted_cipher_suites:
                    cipherstr=cipherstr+str(accepted_cipher_suite.cipher_suite.name)+" "
                r.hset(seq,"TLS1_0",cipherstr)
            r.hset(seq,"STATUS",1)
            
        except KeyError:
            r.hset(seq,"STATUS",4)


        # Scan commands that were run with errors
        for scan_command, error in server_scan_result.scan_commands_errors.items():
            r.hset(seq,"STATUS",5)


if __name__ == "__main__":
    runsslyze(int(sys.argv[1]))
