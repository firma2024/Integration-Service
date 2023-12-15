package com.firma.integracion.DTO;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.Date;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor

public class ProcessDTO {
    private long processId;
    private LocalDateTime dateProcess;
    private LocalDateTime dateLastAction;
    private String office;
    private String department;
    private String legalSubjects;
}
