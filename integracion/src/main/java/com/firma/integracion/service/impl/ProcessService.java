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

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.springframework.stereotype.Service;

import java.io.IOException;
import java.time.LocalDateTime;

@Service
public class ProcessService implements IProcessService {
    @Value("${url.cpnu}")
    private String urlCPNU;
    @Value("${url.cpnu.single}")
    private String urlCPNUSingle;
    String plaintiffPattern = "Demandante: ([^|]+) \\|";
    String defendantPattern = "Demandado: (.+)$";

    /**
     * @param fileNumber File number of the process.
     * @return Information of the process.
     */
    @Override
    public ProcessDTO getProcess(String fileNumber) throws IOException {
        //Get process informatio by CPNU
        String urlCPNUFileNumber = urlCPNU + fileNumber + "&SoloActivos=true";
        Connection.Response response = Jsoup.connect(urlCPNUFileNumber).ignoreContentType(true).execute();
        String res = response.body();
        JsonObject jsonRes = JsonParser.parseString(res)
                .getAsJsonObject();
        JsonArray processArray = jsonRes.getAsJsonArray("procesos");

        JsonObject jsonObject = processArray.get(0).getAsJsonObject();

        ProcessDTO processDTO = new ProcessDTO();
        processDTO.setFileNumber(fileNumber);
        processDTO.setProcessId(jsonObject.get("idProceso").getAsLong());
        processDTO.setDateProcess(LocalDateTime.parse(jsonObject.get("fechaProceso").getAsString()));
        processDTO.setDateLastAction(LocalDateTime.parse(jsonObject.get("fechaUltimaActuacion").getAsString()));
        processDTO.setOffice(jsonObject.get("despacho").getAsString());
        processDTO.setDepartment(jsonObject.get("departamento").getAsString());
        processDTO.setPlaintiff(extractValue(jsonObject.get("sujetosProcesales").getAsString(), plaintiffPattern));
        processDTO.setDefendant(extractValue(jsonObject.get("sujetosProcesales").getAsString(), defendantPattern));

        //Get process type by specific CPNU
        String urlCPNUSingleProcessId = urlCPNUSingle + jsonObject.get("idProceso").getAsLong();
        Connection.Response responseSingle = Jsoup.connect(urlCPNUSingleProcessId).ignoreContentType(true).execute();
        String resSingle = responseSingle.body();
        JsonObject jsonResSingle = JsonParser.parseString(resSingle).getAsJsonObject();

        processDTO.setProcessType(jsonResSingle.get("tipoProceso").getAsString());

        return processDTO;
    }

    private static String extractValue(String input, String pattern) {
        Pattern p = Pattern.compile(pattern);
        Matcher m = p.matcher(input);

        if (m.find()) {
            return m.group(1).trim();
        } else {
            return "No se encontró";
        }
    }
}
