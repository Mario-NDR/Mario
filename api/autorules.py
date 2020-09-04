from api.ip import ipAnalysis
from api.logger import logger
import re
from lib.data import src_ip
def generate_by_ip(ip):
    if ip not in src_ip:
        original_rule = 'drop ip src_ip any -> dest_ip any (msg:"联防-自学习 src_ip -> dest_ip"; sid:sid_num; classtype:system-call-detect; )\n'
        src_defense = original_rule.replace("src_ip",ip).replace("dest_ip","any")
        dest_defense = original_rule.replace("dest_ip",ip).replace("src_ip","any")
        with open("./ThirPath/suricata/marioips/rules/local.rules",'r') as original_rules_file:
            last_rules = original_rules_file.readlines()[-1]
            last_rules_sid = re.findall(r'sid:(.*?);', last_rules, re.S)[0].strip()
            original_rules_file.seek(0)
            if ip not in original_rules_file.read():
                with open ("./ThirPath/suricata/marioips/rules/local.rules",'a+') as new_rules_file:
                    new_rules_file.write(src_defense.replace('sid_num',str(int(last_rules_sid)+1)))
                    new_rules_file.write(dest_defense.replace('sid_num',str(int(last_rules_sid)+2)))
