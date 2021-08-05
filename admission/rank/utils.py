def getProbabilityString(rank, cutoff, total_seats):
    """
    rank < cut_off -  40% of total_seat    => very high chance
    rank < cut_off -  10% of total_seat    => high chance
    rank < cut_off +- 10% of total_seat    => Critical
    rank < cut_off +  30% of total_seat    => low
    ELSE                                   => very low

    cutoff represents cutoff of year 2077 and if other data are present,
    may represet average of cutoffs of different year

    """
    if rank < cutoff - 0.4 * total_seats:
        return "very high"
    elif rank < cutoff - 0.1 * total_seats:
        return "high"
    elif rank > cutoff - 0.1 * total_seats and rank < cutoff + 0.1 * total_seats:
        return "critical"
    elif rank < cutoff + 0.3 * total_seats:
        return "low"
    else:
        return "very low"
