package io.github.lagom130.lab.service;

import io.github.lagom130.lab.config.WorkDayConfig;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class WorkdayService {
    @Resource
    WorkDayConfig workDayConfig;

    public long getWorkdayCountBetween(String startDateStr, String endDateStr) {
        LocalDate startDate = StringUtils.hasLength(startDateStr)?LocalDate.parse(startDateStr):LocalDate.now();
        LocalDate endDate = StringUtils.hasLength(endDateStr)?LocalDate.parse(endDateStr):LocalDate.now();
        return startDate.datesUntil(endDate)
                .filter(date -> workDayConfig.getCustomWorkdayDict().getOrDefault(date.toString(),
                        workDayConfig.getDayOfWeekIsWorkdayDict().getOrDefault(date.getDayOfWeek().getValue(),
                                false)))
                .count();
    }

    public List<LocalDate> getWorkdayListBetween(String startDateStr, String endDateStr) {
        LocalDate startDate = StringUtils.hasLength(startDateStr)?LocalDate.parse(startDateStr):LocalDate.now();
        LocalDate endDate = StringUtils.hasLength(endDateStr)?LocalDate.parse(endDateStr):LocalDate.now();
        return startDate.datesUntil(endDate)
                .filter(date -> workDayConfig.getCustomWorkdayDict().getOrDefault(date.toString(),
                        workDayConfig.getDayOfWeekIsWorkdayDict().getOrDefault(date.getDayOfWeek().getValue(),
                                false)))
                .collect(Collectors.toList());
    }
}
