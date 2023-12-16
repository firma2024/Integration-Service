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
        List<String> wordsList = new ArrayList<>(Arrays.asList(nameDespacho.split("\\s+")));
        String city = wordsList.get(wordsList.size() - 1);

        FirefoxOptions options = new FirefoxOptions();
        options.addArguments("--headless"); // Ejecutar en modo headless
        WebDriver driver = new FirefoxDriver(options);

        driver.get(urlJuzgado);

        List<WebElement> links = driver.findElements(By.tagName("a"));

        for (WebElement link : links) {
            String text = link.getText();
            if (text.toLowerCase().contains(city.toLowerCase())) {
                link.click();
                break;
            }
        }

        Thread.sleep(3000);

        String valueDespacho = wordsList.get(1);

        links = driver.findElements(By.tagName("a"));
        for (WebElement link : links) {
            String text = link.getText();
            String href = link.getAttribute("href");
            if (text.toLowerCase().contains(valueDespacho.toLowerCase())) {
                return href;
            }
        }

        driver.quit();
        return null;
    }
}
