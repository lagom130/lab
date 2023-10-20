package io.github.lagom130.lab.service;

import io.github.lagom130.lab.config.WorkDayConfig;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Service
public class WorkdayService {
    @Resource
    WorkDayConfig workDayConfig;

    public long getWorkdayCountBetween(String startDateStr, String endDateStr) {
        LocalDate startDate = StringUtils.hasLength(startDateStr)?LocalDate.parse(startDateStr):LocalDate.now();
        LocalDate endDate = StringUtils.hasLength(endDateStr)?LocalDate.parse(endDateStr):LocalDate.now();
        // Calculate the number of days between start and end dates
        long daysBetween = (endDate.isAfter(startDate) ? endDate.toEpochDay() - startDate.toEpochDay() : 0);

        // Calculate the number of workdays between start and end dates
        long workdayCount = 0;
        for (int i = 0; i < daysBetween; i++) {
            LocalDate currentDate = startDate.plusDays(i);
            if (workDayConfig.getCustomWorkdayDict().getOrDefault(currentDate.toString(),
                    workDayConfig.getDayOfWeekIsWorkdayDict().getOrDefault(currentDate.getDayOfWeek().getValue(), false))) {
                workdayCount++;
            }
        }

        return workdayCount;
    }

    public List<LocalDate> getWorkdayListBetween(String startDateStr, String endDateStr) {
        LocalDate startDate = StringUtils.hasLength(startDateStr)?LocalDate.parse(startDateStr):LocalDate.now();
        LocalDate endDate = StringUtils.hasLength(endDateStr)?LocalDate.parse(endDateStr):LocalDate.now();
        // Calculate the number of days between start and end dates
        long daysBetween = (endDate.isAfter(startDate) ? endDate.toEpochDay() - startDate.toEpochDay() : 0);

        // Create a list of workdays between start and end dates
        List<LocalDate> workdayList = new ArrayList<>();
        for (int i = 0; i < daysBetween; i++) {
            LocalDate currentDate = startDate.plusDays(i);
            if (workDayConfig.getCustomWorkdayDict().getOrDefault(currentDate.toString(),
                    workDayConfig.getDayOfWeekIsWorkdayDict().getOrDefault(currentDate.getDayOfWeek().getValue(), false))) {
                workdayList.add(currentDate);
            }
        }

        return workdayList;
    }
}
