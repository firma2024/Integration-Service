package com.firma.integracion.controller;

import com.firma.integracion.DTO.ProcessDTO;
import com.firma.integracion.service.intf.IProcessService;
import com.firma.integracion.service.intf.ISeleniumService;
import com.firma.integracion.service.intf.IWebScraperService;
import org.jsoup.HttpStatusException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import java.io.IOException;
import java.net.ConnectException;
import java.util.Optional;

@Controller
@RequestMapping("/api/v1/integration/")
public class IntegrationController {

    @Autowired
    private IWebScraperService webScraperService;
    @Autowired
    private ISeleniumService seleniumService;
    @Autowired
    private IProcessService processService;


    @GetMapping("/getUrl/despacho={nameDespacho}")
    public ResponseEntity<?> getUrlDespacho(@PathVariable String nameDespacho) {
        try {
            String urlJuzgado = webScraperService.getUrlJuzgado(nameDespacho);
            String urlDespacho = seleniumService.getUrlJuzgado(nameDespacho, urlJuzgado);
            String urlEstados = webScraperService.getUrlEstados(urlDespacho);
            return ResponseEntity.ok(urlEstados);
        } catch (IOException e) {
            return ResponseEntity.badRequest().body("Error al obtener la url del juzgado");
        } catch (InterruptedException e) {
            return ResponseEntity.badRequest().body("Error al esperar los despachos");
        }
    }
    @GetMapping("/getProcess/fileNumber={fileNumber}")
    public ResponseEntity<?> getProcessByFileNumber (@PathVariable String fileNumber) throws IOException {
        try{
            return ResponseEntity.ok(processService.getProcess(fileNumber));
        } catch (HttpStatusException e){
            return ResponseEntity.notFound().build();
        } catch (ConnectException e){
            return ResponseEntity.status(408).build();
        }

    }

}
