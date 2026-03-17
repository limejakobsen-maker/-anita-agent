
try:
    @heal
    def parse_json(json_string):
        """
        Parser JSON-data
        Kan feile med ulike exceptions
        """
        import json
        print("[JSON] Parser JSON...")
        return json.loads(json_string)
    
except JSONDecodeError as e:
    print(f"Håndtert feil: {e}")
    # TODO: Legg til passende fallback
    pass
