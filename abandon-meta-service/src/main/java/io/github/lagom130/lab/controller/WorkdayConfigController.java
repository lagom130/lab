package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.dto.WorkdayCustomDTO;
import io.github.lagom130.lab.dto.WorkdayFlagDTO;
import jakarta.websocket.server.PathParam;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 工作日配置
 *
 * @author lujc
 * @date 2023/10/20.
 */
@RestController
@RequestMapping("/workdays/config")
public class WorkdayConfigController {

    @PostMapping("/default/day-of-week/{dayOfWeek}")
    public void upsertWorkdayDefault(@PathParam("dayOfWeek") Integer dayOfWeek, @RequestBody WorkdayFlagDTO dto) {

    }

    @GetMapping("/default/day-of-week")
    public void getWorkdayDefault() {

    }

    @GetMapping("/custom")
    public void getWorkdayCustom() {

    }

    @GetMapping("/custom/{date}")
    public void getWorkdayCustomByDate(@PathParam("date") String date) {

    }

    @DeleteMapping("/custom/{date}")
    public void deleteWorkdayCustomByDate(@PathParam("date") String date) {

    }

    @PostMapping("/custom")
    public void updateWorkdayCustom(@RequestBody List<WorkdayCustomDTO> dtoList) {

    }
}
