package com.firma.integracion.service.impl;

import com.firma.integracion.service.intf.ISeleniumService;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Service
public class SeleniumService implements ISeleniumService {

    @Override
    public String getUrlJuzgado(String nameDespacho, String urlJuzgado) throws InterruptedException {
        System.out.println("Inicio de SeleniumService");
        List<String> listaPalabras = new ArrayList<>(Arrays.asList(nameDespacho.split("\\s+")));
        String ciudad = listaPalabras.get(listaPalabras.size() - 1);

        FirefoxOptions options = new FirefoxOptions();
        options.addArguments("--headless"); // Ejecutar en modo headless
        WebDriver driver = new FirefoxDriver(options);

        driver.get(urlJuzgado);

        List<WebElement> enlaces = driver.findElements(By.tagName("a"));

        for (WebElement enlace : enlaces) {
            String texto = enlace.getText();
            if (texto.toLowerCase().contains(ciudad.toLowerCase())) {
                enlace.click();
                break;
            }
        }

        Thread.sleep(3000);

        String valorDespacho = listaPalabras.get(1);

        enlaces = driver.findElements(By.tagName("a"));
        for (WebElement enlace : enlaces) {
            String texto = enlace.getText();
            String enlaceUrl = enlace.getAttribute("href");
            if (texto.toLowerCase().contains(valorDespacho.toLowerCase())) {
                return enlaceUrl;
            }
        }

        driver.quit();
        return null;
    }
}
