package com.firma.integracion.service.impl;

import com.firma.integracion.DTO.ProcessDTO;
import com.firma.integracion.service.intf.IProcessService;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.json.GsonJsonParser;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.time.LocalDateTime;

@Service
public class ProcessService implements IProcessService {
    @Value("${url.cpnu}")
    private String urlCPNU;
    /**
     * @param fileNumber File number of the process.
     * @return Information of the process.
     */
    @Override
    public ProcessDTO getProcess(String fileNumber) throws IOException {
        String urlCPNUFileNumber = urlCPNU+fileNumber+"&SoloActivos=true";
        Connection.Response response = Jsoup.connect(urlCPNUFileNumber).ignoreContentType(true).execute();
        String res = response.body();
        JsonObject jsonRes = JsonParser.parseString(res)
                .getAsJsonObject();
        ProcessDTO processDTO = new ProcessDTO();
        JsonArray processArray = jsonRes.getAsJsonArray("procesos");

        JsonObject jsonObject = processArray.get(0).getAsJsonObject();
        processDTO.setProcessId(jsonObject.get("idProceso").getAsLong());
        processDTO.setDateProcess(LocalDateTime.parse(jsonObject.get("fechaProceso").getAsString()));
        processDTO.setDateLastAction(LocalDateTime.parse(jsonObject.get("fechaUltimaActuacion").getAsString()));
        processDTO.setOffice(jsonObject.get("despacho").getAsString());
        processDTO.setDepartment(jsonObject.get("departamento").getAsString());
        processDTO.setLegalSubjects(jsonObject.get("departamento").getAsString());

        return processDTO;
    }
}
