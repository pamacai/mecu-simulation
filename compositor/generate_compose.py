import ipaddress
import sys
import yaml

def generate_dns_zone_file(num_hosts, subnet, base_hostname="host", domain="example.com"):
    net = ipaddress.ip_network(subnet)
    usable_hosts = list(net.hosts())

    with open("db.example.com", "w") as dns_file:
        dns_file.write("$TTL    604800\n")
        dns_file.write(f"@    IN    SOA    ns.{domain}. admin.{domain}. (\n")
        dns_file.write("             2         ; Serial\n")
        dns_file.write("         604800         ; Refresh\n")
        dns_file.write("          86400         ; Retry\n")
        dns_file.write("        2419200         ; Expire\n")
        dns_file.write("         604800 )       ; Negative Cache TTL\n")
        dns_file.write(";\n")
        dns_file.write(f"@    IN    NS    ns.{domain}.\n")
        dns_file.write(f"ns    IN    A     {usable_hosts[0]}\n")  # Assuming the first host is the DNS server

        for i in range(1, num_hosts + 1):
            host_ip = usable_hosts[i]
            hostname = f"{base_hostname}{i}"
            dns_file.write(f"{hostname}    IN    A    {host_ip}\n")

def generate_docker_compose(subnet, num_hosts):
    net = ipaddress.ip_network(subnet)
    usable_hosts = list(net.hosts())

    if num_hosts > len(usable_hosts) - 1:  # Reserving the first IP for DNS server
        print("Error: Number of hosts exceeds available IP addresses in the subnet.")
        return

    services = {
        "version": '3.8',
        "services": {},
        "networks": {
            "my_custom_network": {
                "driver": "bridge",
                "ipam": {
                    "config": [{"subnet": subnet}]
                }
            }
        }
    }

    # DNS Server Service
    services["services"]["dns-server"] = {
        "image": "my-dns-server",
        "container_name": "dns-server",
        "hostname": "ns.example.com",
        "networks": {
            "my_custom_network": {
                "ipv4_address": str(usable_hosts[0])
            }
        },
        "volumes": [
            "./db.example.com:/etc/bind/db.example.com"
        ]
    }

    for i in range(1, num_hosts + 1):
        host_ip = usable_hosts[i]
        service_name = f"host{i}"
        services["services"][service_name] = {
            "image": "ubuntu:20.04",
            "container_name": service_name,
            "hostname": f"{service_name}.example.com",
            "networks": {
                "my_custom_network": {
                    "ipv4_address": str(host_ip)
                }
            },
            "command": "tail -f /dev/null"
        }

    return services

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_compose.py <subnet> <num_hosts>")
        sys.exit(1)

    subnet = sys.argv[1]
    num_hosts = int(sys.argv[2])
    base_hostname = "host"
    domain = "example.com"

    # Generate DNS zone file
    generate_dns_zone_file(num_hosts, subnet, base_hostname, domain)

    # Generate Docker Compose file
    compose_content = generate_docker_compose(subnet, num_hosts + 1)  # +1 for DNS server
    if compose_content:
        with open("docker-compose.yml", "w") as file:
            yaml.dump(compose_content, file, default_flow_style=False)

        print("docker-compose.yml and db.example.com files have been generated.")