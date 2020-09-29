import fenixedu
import config
fen_config = fenixedu.FenixEduConfiguration(config.FENIX_CLIENT_ID, config.FENIX_REDIRECT_URI,
                                            config.FENIX_CLIENT_SECRET, config.FENIX_BASE_URL)
fenix_client = fenixedu.FenixEduClient(fen_config)