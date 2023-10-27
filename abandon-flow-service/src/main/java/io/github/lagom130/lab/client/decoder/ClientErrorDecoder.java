package io.github.lagom130.lab.client.decoder;

import feign.Response;
import feign.codec.ErrorDecoder;
import io.github.lagom130.lab.globalResponse.BizException;

public class ClientErrorDecoder implements ErrorDecoder {
    @Override
    public Exception decode(String s, Response response) {
        return new BizException(response.status(), response.reason());
    }
}
