package io.github.lagom130.lab.controller

import io.github.lagom130.lab.dto.MessageTemplateDTO
import io.github.lagom130.lab.globalResponse.ResultUtils
import io.github.lagom130.lab.service.IMessageTemplateService
import io.github.lagom130.lab.vo.MessageTemplateVO
import io.github130.lab.cat.globalResponse.GlobalResult
import jakarta.annotation.Resource
import org.springframework.web.bind.annotation.DeleteMapping
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.PutMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/templates")
class TemplateController {
    @Resource
    private lateinit var messageTemplateService: IMessageTemplateService;

    @PostMapping("")
    fun addOne(@RequestBody dto:MessageTemplateDTO):GlobalResult<Long> {
        return ResultUtils.success(200,"success",messageTemplateService.addOne(dto))
    }

    @PutMapping("/{id}")
    fun updateOne(@PathVariable("id")id: Long, @RequestBody dto: MessageTemplateDTO):GlobalResult<Void> {
        messageTemplateService.updateOne(id,dto)
        return ResultUtils.success(200,"success")
    }


    @GetMapping("/{id}")
    fun getOne(@PathVariable("id") id: Long):GlobalResult<MessageTemplateVO?> {
        return ResultUtils.success(200,"success",messageTemplateService.getOne(id))
    }

    @DeleteMapping("/{id}")
    fun deleteOne(@PathVariable("id")id: Long):GlobalResult<Void> {
        messageTemplateService.deleteOne(id)
        return ResultUtils.success(200,"success")
    }
}