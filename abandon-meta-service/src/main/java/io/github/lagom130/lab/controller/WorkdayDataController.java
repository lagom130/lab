package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.dto.WorkdayCustomDTO;
import io.github.lagom130.lab.dto.WorkdayFlagDTO;
import jakarta.websocket.server.PathParam;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 工作日数据
 *
 * @author lujc
 * @date 2023/10/20.
 */
@RestController
@RequestMapping("/workdays/data")
public class WorkdayDataController {

    @GetMapping("/date/{date}")
    public void getByDate(@PathParam("date") String date) {

    }

    @GetMapping("/date/from/{startDate}/to/{endDate}")
    public void getByDateBetween(@PathParam("startDate") String startDate, @PathParam("endDate") String endDate) {

    }

    @GetMapping("/date/from/{startDate}/to/{endDate}/count")
    public void getCountByDateBetween(@PathParam("startDate") String startDate, @PathParam("endDate") String endDate) {

    }

}
