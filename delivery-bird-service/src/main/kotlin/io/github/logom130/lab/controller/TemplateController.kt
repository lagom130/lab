package io.github.logom130.lab.controller

import io.github.logom130.lab.dto.MessageTemplateDTO
import io.github.logom130.lab.globalResponse.ResultUtils
import io.github.logom130.lab.service.IMessageTemplateService
import io.github130.lab.cat.globalResponse.GlobalResult
import jakarta.annotation.Resource
import org.springframework.web.bind.annotation.DeleteMapping
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.PutMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/template")
class TemplateController {
    @Resource
    private lateinit var messageTemplateService: IMessageTemplateService;

    @PostMapping("")
    fun addOne(dto:MessageTemplateDTO):GlobalResult<Long> {
        return ResultUtils.success(200,"success",-1L)
    }

    @PutMapping("/{id}")
    fun updateOne(id: Long, dto: MessageTemplateDTO):GlobalResult<Long> {
        return ResultUtils.success(200,"success",-1L)
    }


    @GetMapping("/{id}")
    fun getOne(id: Long):GlobalResult<Long> {
        return ResultUtils.success(200,"success",-1L)
    }

    @DeleteMapping("/{id}")
    fun deleteOne(id: Long):GlobalResult<Long> {
        return ResultUtils.success(200,"success",-1L)
    }
}