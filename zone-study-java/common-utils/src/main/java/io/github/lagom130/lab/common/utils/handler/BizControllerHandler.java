package io.github.lagom130.lab.common.utils.handler;


import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;


/**
 * 异常捕获区分新老代码，此切面仅针对业务接口
 */
@Slf4j
@RestControllerAdvice
public class BizControllerHandler extends ResponseEntityExceptionHandler {
	@Resource
	ErrorMessageConfig errorMessageConfig;

	private ObjectMapper objectMapper = new ObjectMapper();


	private final Logger logger =LoggerFactory.getLogger(BizControllerHandler.class);

    @ExceptionHandler
    public ResponseEntity<Object> badRequest(HttpServletRequest request, Exception exception) {
    	logger.error("业务接口全局异常捕获", exception);
    	if (exception instanceof IllegalArgumentException) {
			try {
				BizErrorResultTO resultTO = objectMapper.readValue(exception.getMessage(), BizErrorResultTO.class);
				return ResponseEntity.badRequest()
						.contentType(MediaType.APPLICATION_JSON)
						.body(resultTO);
			} catch (Exception e) {
				logger.error("转换失败",e);
			}
			return ResponseEntity.badRequest()
					.contentType(MediaType.APPLICATION_JSON)
					.body(exception.getMessage());
		} else{
			BizErrorResultTO resultTO = BizErrorResultTO.create500Instance(errorMessageConfig.get500ErrorInfo());
			return ResponseEntity.internalServerError()
					.contentType(MediaType.APPLICATION_JSON)
					.body(resultTO);
    	}
    }
}
