from collections import OrderedDict


router1 = {
  "brand": "Cisco",
  "model": "1941",
  "mgmtIP": "10.0.0.1",
  "G0/0" : "10.0.1.1",
  "G0/1" : "10.0.2.1",
  "G0/2" : "10.1.0.1"
}
router1_OD= OrderedDict([("brand","Cisco"),("model","1941"),("mgmtIP","10.0.0.1"),("G0/0" ,"10.0.1.1"),("G0/1","10.0.2.1",),("G0/2","10.1.0.1")])

for item in router1_OD.items():
    #print(item)
    print(f"key={item[0]}\t\tValue={item[1]}")

interface = OrderedDict([('name', 'GigabitEthernet1'),
                         ('description', 'to port6.sandbox-backend'),
                         ('type',OrderedDict([
                             ('@xmlns:ianaift', 'urn:ietf:params:xml:ns:yang:iana-if-type'),
                             ('#text', 'ianaift:ethernetCsmacd')
                             ])
                          ),
                         ('enabled', 'true'),
                         ('ipv4', OrderedDict([
                             ('@xmlns', 'urn:ietf:params:xml:ns:yang:ietf-ip'),
                             ('address', OrderedDict([
                                 ('ip', '10.10.20.175'),
                                 ('netmask', '255.255.255.0')
                                 ])
                              )]
                                              )
                          ),
                         ('ipv6', OrderedDict([
                             ('@xmlns', 'urn:ietf:params:xml:ns:yang:ietf-ip')]
                                              )
                          )
                         ])


print(interface['name'] + "\t"+interface['type']['#text'] + "\t"+interface['ipv4']['address']['ip'] + "\t" + interface['ipv4']['address']['netmask'])