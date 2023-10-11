package io.github.lagom130.abandon.canary.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/provider")
public class ProviderController {
    @GetMapping("/echo/{str}")
    public String echo(@PathVariable("str") String str) {
        return "Hello Nacos Discovery " + str;
    }
}
