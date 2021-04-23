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
    scan_runner(seq,hostname)
    return


def scan_runner(seq,host):
    hostname=host.decode("utf-8")
    servers_to_scan = []
    server_location = None
    try:
        if r.hget(seq,"ipaddr"):
            server_location = ServerNetworkLocationViaDirectConnection(hostname, 443, r.hget(seq,"ipaddr").decode("utf-8"))
        else:
            server_location = ServerNetworkLocationViaDirectConnection.with_ip_address_lookup(hostname, 443)
            r.hset(seq,"ipaddr",server_location.ip_address)
        #Initialize with hostname, port int and ip address str 
        #print(server_location)
    except Exception as e:
        return
    try:
        server_info = ServerConnectivityTester().perform(server_location)
        servers_to_scan.append(server_info)
    except ConnectionToServerFailed as e:
        return

    scanner = Scanner()

    # Then queue some scan commands for each server
    for server_info in servers_to_scan:
        server_scan_req = ServerScanRequest(
            server_info=server_info, scan_commands={ScanCommand.TLS_1_3_EARLY_DATA},
        )
        scanner.queue_scan(server_scan_req)

    # Then retrieve the result of the scan commands for each server
    for server_scan_result in scanner.get_results():
        try:
            if server_scan_result.scan_commands_results[ScanCommand.TLS_1_3_EARLY_DATA].supports_early_data:
                r.hset(seq,"early","TRUE")

        except KeyError:
            return



if __name__ == "__main__":
    runsslyze(int(sys.argv[1]))
