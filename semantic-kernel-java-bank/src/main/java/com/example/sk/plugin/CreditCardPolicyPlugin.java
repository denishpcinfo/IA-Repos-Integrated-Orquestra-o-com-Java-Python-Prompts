package com.example.sk.plugin;
public class CreditCardPolicyPlugin {

  public String decide(String customerTier, boolean hasOpenDispute) {
    if (hasOpenDispute) return "DENY: open dispute";
    if ("VIP".equalsIgnoreCase(customerTier)) return "ALLOW: VIP";
    return "ALLOW";
  }

}
