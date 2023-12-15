package com.firma.integracion.service.intf;

import com.firma.integracion.DTO.ProcessDTO;
import org.springframework.stereotype.Service;

import java.io.IOException;

@Service
public interface IProcessService {
    ProcessDTO getProcess(String fileNumber) throws IOException;
}
