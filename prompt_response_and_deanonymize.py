from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine, OperatorConfig
from presidio_anonymizer.operators import Operator, OperatorType
from typing import Dict
from pprint import pprint
import json
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64

class InstanceCounterDeanonymizer(Operator):
    def operate(self, text: str, params: Dict = None) -> str:
        """Anonymize the input text."""
        entity_type: str = params["entity_type"]
        # entity_mapping is a dict of dicts containing mappings per entity type
        entity_mapping: Dict[Dict:str] = params["entity_mapping"]
        if entity_type not in entity_mapping:
            raise ValueError(f"Entity type {entity_type} not found in entity mapping!")
        if text not in entity_mapping[entity_type].values():
            raise ValueError(f"Text {text} not found in entity mapping for entity type {entity_type}!")
        return self._find_key_by_value(entity_mapping[entity_type], text)
    @staticmethod
    def _find_key_by_value(entity_mapping, value):
        for key, val in entity_mapping.items():
            if val == value:
                return key
        return None
    def validate(self, params: Dict = None) -> None:
        if "entity_mapping" not in params:
            raise ValueError("An input Dict called `entity_mapping` is required.")
        if "entity_type" not in params:
            raise ValueError("An entity_type param is required.")
    def operator_name(self) -> str:
        return "entity_counter_deanonymizer"
    def operator_type(self) -> OperatorType:
        return OperatorType.Deanonymize

def decode_dict_and_string_from_file(file_name):
    with open(file_name, "r") as file:
        encoded_string = file.read()
    # Decode Base64 to JSON string
    decoded_bytes = base64.b64decode(encoded_string.encode("utf-8"))
    decoded_json_string = decoded_bytes.decode("utf-8")
    # Convert JSON string back to dictionary
    combined = json.loads(decoded_json_string)
    print("Decoding Encrypted entity mapping and Anonymized text from 'encoded.txt'.")
    return combined["dictionary"], combined["text"]

def decrypt_value(encrypted_b64):
    # Hardcoded key
    key = b'\xb4R\xf0C\x90\xe8\xe4\x08\x00\xadCCL\xb2H}\xbb\x87g\x97\xd4e\x99o\x16\xebK\x9dN\x88sR'
    aesgcm = AESGCM(key)
    # Decode base64
    encrypted = base64.b64decode(encrypted_b64)
    # First 12 bytes = nonce
    nonce = encrypted[:12]
    ciphertext = encrypted[12:]
    # Decrypt
    return aesgcm.decrypt(nonce, ciphertext, None).decode()

def deanonymize_text(text, mapping):
    i = 0
    deanonymized_text = ""
    while(i < len(text)):
        if(text[i] == '<'):
            temp = i
            while((temp < len(text)) and (text[temp] != '>')):
                temp += 1
            if(text[i: (temp + 1)] in mapping):
                deanonymized_text += mapping[text[i: (temp + 1)]]
                i = temp
            else:
                deanonymized_text += text[i]
        else:
            deanonymized_text += text[i]
        i += 1
    return deanonymized_text

extracted_entity_mapping, extracted_anonymized_text = decode_dict_and_string_from_file("encoded.txt")
print("\nExtracted entity mapping:")
pprint(extracted_entity_mapping)
# Decrypt all values
decrypted_entity_mapping = {k: decrypt_value(v) for k, v in extracted_entity_mapping.items()}
print("\nExtracted entity mapping:")
pprint(decrypted_entity_mapping)
print("\nExtracted anonymized text:")
print(extracted_anonymized_text)
#text = "<PERSON_4>, a <DATE_TIME_6> software engineer born on <DATE_TIME_5>, lives at 742 Evergreen Terrace, Apartment 5B, <LOCATION_2>, IL 62704. Contacts: <EMAIL_ADDRESS_2>, <EMAIL_ADDRESS_1>, <PHONE_NUMBER_5>, <PHONE_NUMBER_4>, <URL_1>, social media username “john_smith42.” IDs: <DATE_TIME_4> (SSN), <US_DRIVER_LICENSE_2> (driver’s license), <US_DRIVER_LICENSE_1> (passport). Financial: <UK_NHS_1> (checking), <US_BANK_NUMBER_1> (routing), Mastercard ending 9876 (<DATE_TIME_3> expiration). Medical: <US_PASSPORT_1>. Emergency contacts: <PERSON_3> (<PHONE_NUMBER_3>), <PERSON_2> (<PHONE_NUMBER_2>). Security: 2FA via phone and email. Other: packages (tracking 1Z999AA10123456784), loyalty program <PHONE_NUMBER_1>, ride-share services, taxpayer ID <US_ITIN_1>."
text = input("\nEnter an anonymous response: ")
# pprint(anonymized_result.text)
print("\nDe-anonymized response:")
print(deanonymize_text(text, decrypted_entity_mapping))