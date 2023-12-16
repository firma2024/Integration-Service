package com.firma.integracion.service.intf;

import org.springframework.stereotype.Service;

import java.io.IOException;


@Service
public interface IWebScraperService {
    public String getUrlJuzgado(String nameDespacho) throws IOException;
    public String getUrlEstados(String urlDespacho) throws IOException;
}
