def getBotKey(  ):
    try:
        from configparser import ConfigParser
        config = ConfigParser()
        config.read("./env.conf", encoding='UTF-8')
        key_data = config.get("general","bot_key")
        return key_data
    except Exception as e:
        return ''