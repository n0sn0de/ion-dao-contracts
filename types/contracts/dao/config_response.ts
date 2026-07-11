import { Addr, Config } from "./shared-types";

export interface ConfigResponse {
  config: Config;
  gov_token: string;
  /**
   * Proposals submitted at or before this height have quarantined deposit claims.
   */
  legacy_deposit_claim_cutoff_height?: number | null;
  staking_contract: Addr;
  [k: string]: unknown;
}
