def convert_time(time: float) -> str:
    """
    Converts time in seconds to a string in the “MM:SS:MMM” (minutes:seconds:milliseconds) format.

    Examples:
        convert_time(123.123) => '02:03:123'
        convert_time(543.345) => '09:03:345'

    :param time: The time value in seconds
    :return: The formatted time string in the "MM:SS:MMM" (minutes:seconds:milliseconds) format.
    """
    minutes = int(time // 60)
    seconds = int(time % 60)
    ms = int(round((time % 1) * 1000))

    return f"{minutes:02d}:{seconds:02d}:{ms:03d}"
