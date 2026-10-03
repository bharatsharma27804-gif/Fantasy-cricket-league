def calculate_player_points(match_row):
    """
    match_row schema:
    [player, scored, faced, fours, sixes, bowled, maiden, given, wkts, catches, stumping, ro]
    """
    if not match_row:
        return 0

    player, scored, faced, fours, sixes, bowled, maiden, given, wkts, catches, stumping, ro = match_row
    points = 0.0

    # 1. Batting Rules
    points += scored / 2.0  # 1 point for every 2 runs
    if scored >= 100:
        points += 10
    elif scored >= 50:
        points += 5

    sr = (scored / faced * 100) if faced > 0 else 0
    if sr > 100:
        points += 4
    elif 80 <= sr <= 100:
        points += 2

    points += (fours * 1) + (sixes * 2)

    # 2. Bowling Rules
    points += wkts * 10
    if wkts >= 5:
        points += 10
    elif wkts >= 3:
        points += 5

    overs = bowled / 6.0
    if overs > 0:
        econ = given / overs
        if econ < 2:
            points += 10
        elif 2 <= econ <= 3.5:
            points += 7
        elif 3.5 < econ <= 4.5:
            points += 4

    # 3. Fielding Rules
    points += (catches + stumping + ro) * 10

    return int(points)