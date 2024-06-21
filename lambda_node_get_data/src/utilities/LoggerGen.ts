import { BdBLogger } from '@npm-bbta/bbog-dig-dt-tslog-lib';
import { IMaskOptions, TLogLevelName } from '@npm-bbta/bbog-dig-dt-tslog-lib/interfaces';
import config from '../config';

export default class LoggerGen {
  public static getLoggingInstance(fileName: string, maskOptions?: IMaskOptions): BdBLogger {
    return new BdBLogger(
      config.CLOUD_LOGS !== 'false',
      fileName,
      config.LOG_LEVEL as TLogLevelName,
      maskOptions
    );
  }
}
