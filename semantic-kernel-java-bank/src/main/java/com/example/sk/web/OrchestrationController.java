package com.example.sk.web;

import com.example.sk.plugin.CreditCardPolicyPlugin;
import org.slf4j.MDC;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.Map;
import java.util.HashMap;
import java.util.Optional;

@RestController
@RequestMapping("/orchestrate")
public class OrchestrationController {

    private final WebClient python;
    private final CreditCardPolicyPlugin policy = new CreditCardPolicyPlugin();

    public OrchestrationController(WebClient pythonClient) {
        this.python = pythonClient;
    }

    @GetMapping("/plan")
    public Mono<ResponseEntity<Map>> viewPlan(
            @RequestParam(name = "goal") String goal,
            @RequestParam(name = "template", required = false) String template
    ) {
        String cid = Optional.ofNullable(MDC.get("cid")).orElse("-");
        return python.get()
                .uri(uriBuilder -> uriBuilder.path("/plan-q")
                        .queryParam("goal", goal)
                        .queryParamIfPresent("template", Optional.ofNullable(template))
                        .build())
                .header(CorrelationFilter.HEADER, cid)
                .retrieve()
                .bodyToMono(Map.class)
                .map(body -> {
                    if (body instanceof Map) ((Map) body).put("cid", cid);
                    return ResponseEntity.ok(body);
                });
    }

    @PostMapping(value = "/execute", produces = MediaType.APPLICATION_JSON_VALUE)
    public Mono<ResponseEntity<Map<String, Object>>> orchestrate(
            @RequestParam(name = "goal") String goal,
            @RequestParam(name = "template", required = false) String template,
            @RequestParam(name = "tier") String tier,
            @RequestParam(name = "dispute") boolean dispute
    ) {
        String cid = Optional.ofNullable(MDC.get("cid")).orElse("-");
        String decision = policy.decide(tier, dispute);

        if (decision.startsWith("DENY")) {
            Map<String, Object> result = new HashMap<>();
            result.put("cid", cid);
            result.put("decision", decision);
            result.put("executed", Boolean.FALSE);
            result.put("reason", "Policy denied before Python execution");
            return Mono.just(ResponseEntity.ok(result));
        }

        Map<String, Object> body = new HashMap<>();
        body.put("goal", goal);
        body.put("template", template);

        return python.post()
                .uri("/execute")
                .contentType(MediaType.APPLICATION_JSON)
                .header(CorrelationFilter.HEADER, cid)
                .bodyValue(body)
                .retrieve()
                .bodyToMono(Map.class)
                .map(report -> {
                    Map<String, Object> out = new HashMap<>();
                    out.put("cid", cid);
                    out.put("decision", decision);
                    out.put("executed", Boolean.TRUE);
                    out.put("python_report", report);
                    return ResponseEntity.ok(out);
                });
    }
}
