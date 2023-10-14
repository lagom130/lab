package io.github.lagom130.lab.abandon.order.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient("canary-account")
public interface AccountClient {
    @PostMapping("account/{userId}/debit")
    String debit(@PathVariable("userId")String userId, @RequestParam("money")int money);
}
