package io.github.lagom130.lab.service;

import jakarta.websocket.server.PathParam;
import org.apache.commons.lang.time.DateUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;

/**
 * 工作日数据
 *
 * @author lujc
 * @date 2023/10/20.
 */
public class WorkdayDataService {

    public void getByDate(String date) {

    }

    public void getByDateBetween(String startDateStr, String endDateStr) {
        LocalDate startDate = LocalDate.parse(startDateStr);
        LocalDate endDate = LocalDate.parse(endDateStr);
    }

    public void getCountByDateBetween(String startDateStr, String endDateStr) {
        LocalDate startDate = LocalDate.parse(startDateStr);
        LocalDate endDate = LocalDate.parse(endDateStr);
    }

}
