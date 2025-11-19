import numpy as np
import json
import re

def parse_result(age_gate, vendor, result_str, method="Estimation"):
    match vendor:

        case 'IDmission':
            if method=="Estimation":
                try:
                    verification_data = json.loads(result_str)
                    estimated_age = round(float(verification_data[0]['resultData']['estimatedAge']), 2)
                    confidence = round(float(verification_data[0]['resultData']['realScore']), 2)
                    return {'estimate': estimated_age} if estimated_age > 0 else None
                except Exception as err:
                    return None
            
            if method=="Verification":
                try:
                    verification_data = json.loads(result_str)
                    ver_result_string = verification_data[0]['resultData']['verificationResult']
                    
                    if ver_result_string == "Approved":
                        ver_result = True
                    elif ver_result_string == "Under the Age of 18":
                        ver_result = False
                    else:
                        ver_result = False
                    return {18: ver_result}
                except Exception as err:
                    return None

        case 'PrivateId':
            try:
                verification_data = json.loads(result_str)
                estimated_age = round(float(verification_data['age']), 2)
                return {'estimate': estimated_age} if estimated_age > 0 else None
            except Exception as err:
                return None

        case 'VerifyChain':
            try:
                verification_data = json.loads(result_str)
                estimated_age = round(float(verification_data['estimatedAge']), 2)
                confidence = round(float(verification_data['confidence']), 2)
                return {'estimate': estimated_age} if estimated_age > 0 else None
            except Exception as err:
                return None

        case 'IDVerse':
            try:
                verification_data = json.loads(result_str)

                estimated_age = None
                for doc in verification_data['results']['documents']:
                    if estimated_age is None:
                        estimated_age = round(float(doc['calculatedData']['age']), 2)
                    else:
                        return None
                return {'estimate': estimated_age} if estimated_age > 0 else None
            except Exception as err:
                return None

        case 'Unissey':
            try:
                verification_data = json.loads(result_str)
                estimated_age = round(float(verification_data["data"]["details"]["age"]["age_estimation"]["estimated_age"]), 2)
                age_range = verification_data["data"]["details"]["age"]["age_estimation"]["age_range"]
                return {'estimate': estimated_age} if estimated_age > 0 else None
            except Exception as err:
                return None

        case 'Persona':
            if method=="Estimation":
                try:
                    verification_data = json.loads(result_str)

                    estimated_age = round(float(verification_data['data']['attributes']['fields']['selfie-estimated-age']['value']), 2)
                    return {'estimate': estimated_age} if estimated_age > 0 else None

                except Exception as err:
                    return None
            
            if method=="Verification":
                try:
                    verification_data = json.loads(result_str)
                    verified_docs = set()
                    for included_obj in verification_data['included']:
                        if included_obj['type'].startswith('verification/') and included_obj["attributes"]["status"] == "passed":
                            verified_docs.add(included_obj['type'])
                    if len(verified_docs) >= 2:
                        ver_result = True
                    else:
                        ver_result = False
                    return {18: ver_result}

                except Exception as err:
                    return None

        case 'Yoti':
            try:
                verification_data = json.loads(result_str)
                estimated_age = round(float(verification_data["age"]), 2)
                return {'estimate': estimated_age} if estimated_age > 0 else None
            except Exception as err:
                return None

        case 'Rigr-AI':
            try:
                verification_data = json.loads(result_str)
                estimated_age = round(float(verification_data["age"]), 2)
                uncertainty = round(float(verification_data["uncertainty"]), 2)
                return {'estimate': estimated_age} if estimated_age > 0 else None
                
            except Exception as err:
                try:
                    verification_data = json.loads(result_str)
                    estimated_age = round(float(verification_data['response']['results'][0]['results'][0]['age']), 2)
                    uncertainty = round(float(verification_data['response']['results'][0]['results'][0]["uncertainty"]), 2)
                    return {'estimate': estimated_age} if estimated_age > 0 else None
                except Exception as err:
                    return None

        case 'Arissian':
            try:
                verification_data = json.loads(result_str)
                msgData = json.loads(verification_data['MsgData'])

                info_string = msgData['Info']
                age_gate_match = re.match(r".* (target age of (\d+)) .*", info_string)
                age_gate = int(age_gate_match.group(2))

                pass_match = re.match(r".* (\[AE_(PASS|FAIL)\])", info_string)
                bool_check = True if pass_match.group(2) == 'PASS' else False

                confidence_match = re.match(r"(.*) confidence .*", info_string)
                confidence_level = confidence_match.group(1)

                return {age_gate: bool_check}

            except Exception:
                return None

        case 'Needemand':
            try:
                verification_data = json.loads(result_str)
                if age_gate is not None:
                    if verification_data['result'] == '1':
                        return {int(age_gate): True}
                    elif verification_data['result'] == '0':
                        return {int(age_gate): False}
                    else:
                        return None
                else:
                    return None
            except Exception:
                return None

        case 'ShareRing':
            try:
                verification_data = json.loads(result_str)
                ver_msg = verification_data["qrRes"]
                age_gate_match_pos = re.match(r"\nYes, I am (\d+) or over", ver_msg)
                if age_gate_match_pos:
                    age_gate = int(age_gate_match_pos.group(1))
                    return {age_gate: True}
                age_gate_match_neg = re.match(r"\nNo, I'm not over (\d+)", ver_msg)
                if age_gate_match_neg:
                    age_gate = int(age_gate_match_neg.group(1))
                    return {age_gate: False}
                return None
            except Exception:
                return None

        case 'RightCrowd':
            try:
                verification_data = json.loads(result_str)
                age_gate_pass = True if verification_data['result'] == "True" else False
                
                return {int(verification_data['ageThreshold']): age_gate_pass}
            except Exception as err:
                return None

        case 'MyMahi':
            try:
                verification_data = json.loads(result_str)
                age_gate_results = verification_data['age_equal_or_over']
                return {int(age_gate): age_gate_results[age_gate] for age_gate in age_gate_results}
            except Exception as err:
                return None

        case 'VerifyMy':
            try:
                verification_data = json.loads(result_str)
                return {int(age_gate): verification_data['age_verified']}
            except Exception as err:
                return None

        case 'Privately':
            try:
                verification_data = json.loads(result_str)
                return {int(verification_data["age"]): verification_data["rlt"]}
            except Exception as err:
                return None

        case _:
            return None
