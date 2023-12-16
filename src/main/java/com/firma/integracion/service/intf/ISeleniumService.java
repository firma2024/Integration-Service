package com.firma.integracion.service.intf;

import org.springframework.stereotype.Service;

@Service
public interface ISeleniumService {
    public String getUrlJuzgado(String nameDespacho, String urlJuzgado) throws InterruptedException;
}
