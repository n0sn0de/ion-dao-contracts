/**
 * Migration from v0.0.1 always quarantines potentially unsafe legacy deposits. There is deliberately no opt-out because distinct v0.0.1 artifacts cannot be distinguished safely from CW2 metadata alone.
 */
export interface MigrateMsg {}
