def generate_position_meta_description(position):
    suffix = "n" if position.position_type.lower().startswith(("a", "e", "i", "o", "u")) else ""
    meta = f"Mozilla is hiring a{suffix} " f"{position.position_type.lower()} {position.title} in "

    if len(position.location_list) > 1:
        meta = meta + f'{", ".join(position.location_list[:-1])} and {position.location_list[-1]}'
    else:
        meta = meta + position.location_list[0]

    return meta
