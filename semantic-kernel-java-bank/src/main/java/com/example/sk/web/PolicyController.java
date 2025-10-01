package com.example.sk.web;

import org.slf4j.MDC;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.example.sk.plugin.CreditCardPolicyPlugin;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/policy")
public class PolicyController {
    private final CreditCardPolicyPlugin plugin = new CreditCardPolicyPlugin();

    @PostMapping("/reissue")
    public ResponseEntity<?> reissue(
            @RequestParam(name = "tier") String tier,
            @RequestParam(name = "dispute") boolean dispute
    ){
        String decision = plugin.decide(tier, dispute);
        String cid = Optional.ofNullable(MDC.get("cid")).orElse("-");

        Map<String, Object> body = new HashMap<>();
        body.put("cid", cid);
        body.put("decision", decision);
        return ResponseEntity.ok().body(body);
    }
}
