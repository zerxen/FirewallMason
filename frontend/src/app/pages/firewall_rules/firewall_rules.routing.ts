/**
 * Created by havrila on 7/1/2017.
 */
import { Routes, RouterModule } from '@angular/router';

import { FirewallRulesComponent } from './firewall_rules.component';

const routes: Routes = [
  {
    path: '',
    component: FirewallRulesComponent,
  },
];

export const routing = RouterModule.forChild(routes);
