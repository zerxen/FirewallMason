import { Injectable } from '@angular/core';

import { BaThemeConfigProvider } from './theme.configProvider';
import { colorHelper } from './theme.constants';

@Injectable()
export class BaThemeConfig {

  constructor(private _baConfig: BaThemeConfigProvider) {
  }
  config() {
    this._baConfig.changeTheme( { name: 'red' } );
    const colorScheme = {
      primary: '#ff7c57',
      info: '#ffa935',
      success: '#78b913',
      warning: '#dedf1b',
      danger: '#f95457',
    };
    this._baConfig.changeColors({
      default: '#4e4e55',
      defaultText: '#e2e2e2',
      border: '#dddddd',
      borderDark: '#aaaaaa',

      primary: colorScheme.primary,
      info: colorScheme.info,
      success: colorScheme.success,
      warning: colorScheme.warning,
      danger: colorScheme.danger,

      primaryLight: colorHelper.tint(colorScheme.primary, 30),
      infoLight: colorHelper.tint(colorScheme.info, 30),
      successLight: colorHelper.tint(colorScheme.success, 30),
      warningLight: colorHelper.tint(colorScheme.warning, 30),
      dangerLight: colorHelper.tint(colorScheme.danger, 30),

      primaryDark: colorHelper.shade(colorScheme.primary, 15),
      infoDark: colorHelper.shade(colorScheme.info, 15),
      successDark: colorHelper.shade(colorScheme.success, 15),
      warningDark: colorHelper.shade(colorScheme.warning, 15),
      dangerDark: colorHelper.shade(colorScheme.danger, 15),

      dashboard: {
        blueStone: '#62000c',
        surfieGreen: '#ff7c57',
        silverTree: '#ffa935',
        gossip: '#ffd38d',
        white: '#ffa935',
      },
    });
  }
}
