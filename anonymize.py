from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine, OperatorConfig
from presidio_anonymizer.operators import Operator, OperatorType
from typing import Dict
from pprint import pprint
import json
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class InstanceCounterAnonymizer(Operator):
    REPLACING_FORMAT = "<{entity_type}_{index}>"
    def operate(self, text: str, params: Dict = None) -> str:
        """Anonymize the input text."""
        entity_type: str = params["entity_type"]
        # entity_mapping is a dict of dicts containing mappings per entity type
        entity_mapping: Dict[Dict:str] = params["entity_mapping"]
        entity_mapping_for_type = entity_mapping.get(entity_type)
        if not entity_mapping_for_type:
            new_text = self.REPLACING_FORMAT.format(
                entity_type=entity_type, index=1
            )
            entity_mapping[entity_type] = {}
        else:
            if text in entity_mapping_for_type:
                return entity_mapping_for_type[text]
            previous_index = self._get_last_index(entity_mapping_for_type)
            new_text = self.REPLACING_FORMAT.format(
                entity_type=entity_type, index=previous_index + 1
            )
        entity_mapping[entity_type][text] = new_text
        return new_text
    @staticmethod
    def _get_last_index(entity_mapping_for_type: Dict) -> int:
        """Get the last index for a given entity type."""
        return len(entity_mapping_for_type)
    def validate(self, params: Dict = None) -> None:
        """Validate operator parameters."""
        if "entity_mapping" not in params:
            raise ValueError("An input Dict called `entity_mapping` is required.")
        if "entity_type" not in params:
            raise ValueError("An entity_type param is required.")
    def operator_name(self) -> str:
        return "entity_counter"
    def operator_type(self) -> OperatorType:
        return OperatorType.Anonymize

def encrypt_value(value):
    # Generate a strong random 32-byte key (256-bit)
    #key = AESGCM.generate_key(bit_length=256)
    #print(key)
    # Hardcoded key
    key = b'\xb4R\xf0C\x90\xe8\xe4\x08\x00\xadCCL\xb2H}\xbb\x87g\x97\xd4e\x99o\x16\xebK\x9dN\x88sR'
    aesgcm = AESGCM(key)
    # Generate a random 12-byte nonce
    nonce = os.urandom(12)
    # Encrypt the value (returns bytes)
    ct = aesgcm.encrypt(nonce, value.encode(), None)
    # Store nonce + ciphertext together and encode in base64
    return base64.b64encode(nonce + ct).decode()

def encode_dict_and_string_to_file(data_dict, text, file_name):
    # Combine dictionary and string into a single dictionary
    combined = {
        "dictionary": data_dict,
        "text": text
    }    
    # Convert combined data to JSON string
    json_string = json.dumps(combined)
    # Encode JSON string to Base64
    encoded_bytes = base64.b64encode(json_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    # Save encoded string to file
    with open(file_name, "w") as file:
        file.write(encoded_string)
    print(f"\nEncrypted entity mapping and Anonymized text encoded and saved to '{file_name}'.")

text = "Johnathan Smith, a 42-year-old software engineer born on February 12, 1984, lives at 742 Evergreen Terrace, Apartment 5B, Springfield, IL 62704. His primary email address is johnathan.smith42@examplemail.com, and his secondary work email is j.smith@techcorpsolutions.com. Johnathan’s personal phone number is (217) 555-0134, while his office line at TechCorp Solutions is (312) 555-9876. He maintains a personal website at www.johnathansmithdev.com and uses the username “john_smith42” on various social media platforms, including Twitter, LinkedIn, and GitHub. His government-issued Social Security Number is formatted as 123-45-6789, and his driver’s license number is S12345678 issued by Illinois DMV. For financial transactions, Johnathan has a checking account at First National Bank under account number 0123456789 and routing number 071000013. He holds a Mastercard ending in 9876 with an expiration date of 08/28. Johnathan also has a passport, number X1234567, which was issued on March 15, 2019, expiring March 14, 2029. His medical records are associated with patient ID 567891234 at Springfield General Hospital, where he has been treated for hypertension and mild asthma. Emergency contacts include his spouse, Emily Smith, reachable at (217) 555-0199, and his brother, Michael Smith, at (312) 555-0245. Johnathan’s online account security relies on a combination of two-factor authentication codes sent to his phone and email. He often receives packages at his home address and uses the tracking number 1Z999AA10123456784 for shipments. His tax records reference taxpayer ID 987-65-4321. He participates in loyalty programs under membership number 1122334455 and frequently uses ride-share services, linking his account to his credit card ending in 9876."
print("Original text:")
print(text)
analyzer = AnalyzerEngine()
analyzer_results = analyzer.analyze(text=text, language="en")
print("\nAnalyzer results:")
pprint(analyzer_results)
# Create Anonymizer engine and add the custom anonymizer
anonymizer_engine = AnonymizerEngine()
anonymizer_engine.add_anonymizer(InstanceCounterAnonymizer)
# Create a mapping between entity types and counters
entity_mapping = dict()
# Anonymize the text
anonymized_result = anonymizer_engine.anonymize(
    text,
    analyzer_results,
    {
        "DEFAULT": OperatorConfig(
            "entity_counter", {"entity_mapping": entity_mapping}
        )
    },
)
print("\nAnonymized text:")
print(anonymized_result.text)
print("\nEntity mapping:")
pprint(entity_mapping, indent=2)
processed_entity_mapping = {v: k for category in entity_mapping.values() for k, v in category.items()}
print("\nProcessed entity mapping:")
pprint(processed_entity_mapping)
# Encrypt all values
encrypted_entity_mapping = {k: encrypt_value(v) for k, v in processed_entity_mapping.items()}
print("\nEncrypted entity mapping:")
pprint(encrypted_entity_mapping)
encode_dict_and_string_to_file(encrypted_entity_mapping, anonymized_result.text, "encoded.txt")
