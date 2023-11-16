package io.github.lagom130.abandon.canary.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/info")
public class InfoController {

    @GetMapping(value = "/a")
    public Map<String, Object> getInfoA(@RequestParam String username) {
        HashMap<String, Object> map = new HashMap<>();
        map.put("username", username);
        map.put("password", "123456");
        return map;
    }
}
