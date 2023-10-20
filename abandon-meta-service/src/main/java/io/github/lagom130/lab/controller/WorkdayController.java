package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.service.WorkdayService;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
public class WorkdayController {
    @Resource
    WorkdayService workdayService;

    @GetMapping("/workdays")
    public Result<List<LocalDate>> getList(@RequestParam("start") String start, @RequestParam("end") String end) {
        return new Result<List<LocalDate>>().success(workdayService.getWorkdayListBetween(start, end));
    }

    @GetMapping("/workdays/count")
    public Result<Long> getCount(@RequestParam("start") String start, @RequestParam("end") String end) {
        return new Result<Long>().success(workdayService.getWorkdayCountBetween(start, end));
    }
}
