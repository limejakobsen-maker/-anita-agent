@heal
def prosess_data(data_list):
    """
    Prosesserer en dataliste
    Kan feile med IndexError hvis listen er tom
    """
    print(f"[DATA] Prosesserer {len(data_list)} elementer...")
    
    # Risikabel operasjon: henter første og siste element
    first = data_list[0] if len(data_list) > 0 else None  # Kan feile hvis tom
    last = data_list[-1]  # Kan feile hvis tom
    
    return {"first": first, "last": last, "count": len(data_list)}
