/**
 * Created by havrila on 7/1/2017.
 */
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { FirewallRulesComponent } from './firewall_rules.component';
import { routing } from './firewall_rules.routing';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    routing,
  ],
  declarations: [
    FirewallRulesComponent,
  ],
})
export class FirewallRulesModule {}
