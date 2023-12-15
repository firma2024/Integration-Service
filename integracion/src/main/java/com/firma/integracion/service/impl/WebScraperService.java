package com.firma.integracion.service.impl;

import com.firma.integracion.service.intf.IWebScraperService;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.TrustManager;
import java.io.IOException;

import javax.net.ssl.*;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.time.LocalDate;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class WebScraperService implements IWebScraperService {

    @Value("${url.rama.judicial}")
    private String urlRamaJudicial;
    @Value("${url.rama.judicial.inicio}")
    private String urlRamaJudicialInicio;

    @Override
    public String getUrlJuzgado(String nameDespacho) throws IOException {
        System.out.println("Inicio de busqueda de link del juzgado");
        List<String> listaPalabras = new ArrayList<>(Arrays.asList(nameDespacho.split("\\s+")));
        int tama = listaPalabras.size();
        listaPalabras.subList(tama - 2, listaPalabras.size()).clear();
        listaPalabras.removeIf(word -> word.matches("\\d+"));
        Map<String, String> mapEnlaces = new ConcurrentHashMap<>();

        trustAllCertificates();
        Connection connection = Jsoup.connect(urlRamaJudicial);
        // Ignorar la verificación SSL
        connection.ignoreHttpErrors(true);
        connection.ignoreContentType(true);

        Document doc = connection.get();

        Elements links = doc.select("a"); // Seleccionar todos los elementos <a>

        for (Element link : links) {
            String href = link.attr("href"); // Obtener el atributo href
            String text = link.text(); // Obtener el texto dentro del elemento <a>
            mapEnlaces.put(text, href);
        }

        boolean containsEjecucion = false;
        boolean containsPromiscuo = false;

        for (String palabra : listaPalabras) {
            if (palabra.toLowerCase().contains("ejecución")) {
                containsEjecucion = true;
            }
            if (palabra.toLowerCase().contains("promiscuo")) {
                containsPromiscuo = true;
            }
            for (String key : mapEnlaces.keySet()){
                if (mapEnlaces.size() == 1){
                    break;
                }
                if (!key.toLowerCase().contains(palabra.toLowerCase())){
                    mapEnlaces.remove(key);
                }
            }
        }

        if (!containsEjecucion){
            for (String key : mapEnlaces.keySet()){
                if (key.toLowerCase().contains("ejecución")){
                    mapEnlaces.remove(key);
                }
            }
        }
        if(!containsPromiscuo){
            for (String key : mapEnlaces.keySet()){
                if (key.toLowerCase().contains("promiscuo")){
                    mapEnlaces.remove(key);
                }
            }
        }

        if (mapEnlaces.size() == 1){
            return mapEnlaces.get(mapEnlaces.keySet().iterator().next());
        }

        return null;
    }

    @Override
    public String getUrlEstados(String urlDespacho) throws IOException {
        System.out.println("Inicio de busqueda de link de estados");
        List<String> enlaces = new ArrayList<>();
        trustAllCertificates();
        System.out.println(urlDespacho);
        Connection connection = Jsoup.connect(urlDespacho);
        // Ignorar la verificación SSL
        connection.ignoreHttpErrors(true);
        connection.ignoreContentType(true);
        int indexEstados = 0;
        String year = String.valueOf(LocalDate.now().getYear());

        Document doc = connection.get();
        Elements elements = doc.getElementsByClass("layouts level-1");
        for (Element element : elements) {
            int i = 0;
            Elements titles = element.select("h4");
            for (Element title : titles) {
                String text = title.text();
                if (text.toLowerCase().contains("Estados Electrónicos".toLowerCase())){
                    indexEstados = i;
                }
                i ++;
            }
            Elements links = element.select("a");
            for (Element link : links) {
                String href = link.attr("href");
                String text = link.text();
                if (text.contains(year)){
                    enlaces.add(href);
                }
            }
        }
        System.out.println("Enviando link de estados");
        return urlRamaJudicialInicio + enlaces.get(indexEstados - 1);
    }

    private void trustAllCertificates() {
        // Crear un gestor de confianza que no realice ninguna verificación de certificados
        TrustManager[] trustAllCerts = new TrustManager[]{
                new X509TrustManager() {
                    public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                        return null;
                    }

                    public void checkClientTrusted(
                            java.security.cert.X509Certificate[] certs, String authType) {
                    }

                    public void checkServerTrusted(
                            java.security.cert.X509Certificate[] certs, String authType) {
                    }
                }
        };

        // Ignorar todas las verificaciones de hostname
        HostnameVerifier allHostsValid = (hostname, session) -> true;

        // Installar el gestor de confianza y el verificador de hostname en la conexión SSL
        try {
            SSLContext sslContext = SSLContext.getInstance("SSL");
            sslContext.init(null, trustAllCerts, new java.security.SecureRandom());

            HttpsURLConnection.setDefaultSSLSocketFactory(sslContext.getSocketFactory());
            HttpsURLConnection.setDefaultHostnameVerifier(allHostsValid);
        } catch (NoSuchAlgorithmException | KeyManagementException e) {
            e.printStackTrace();
        }
    }
}
