<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output method="text"/>
    
    <xsl:template match="unittitle">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="unitdate"/>

    
    <xsl:template match="ead">
        <xsl:variable name="eadid" select="eadheader/eadid"/>
        
        <!-- Template is 
            eadid | null | refid | null | digital object id | digital object title |
            true | service copy link | true | thumbnail link | true-->
        <xsl:for-each select="//daogrp">
            
            <!-- Add eadid -->
            <xsl:value-of select="$eadid"/><xsl:text>|</xsl:text>
            
            <!-- Add three blank columns -->
            <xsl:text>|||</xsl:text>
            
            <!-- Add digital object ID -->
            <xsl:value-of select="../did/unitid"/><xsl:text>|</xsl:text>
            
           <!-- Add digital object title -->
            <xsl:choose>
                <!-- If title is present in the same block as the dao -->
                <xsl:when test="../did/unittitle">
                    <xsl:apply-templates select="../did/unittitle"/><xsl:text>|TRUE|</xsl:text>
                </xsl:when>
                
                <!-- If title is inherited from the parent -->
                <xsl:when test="../../did/unittitle">
                    <xsl:apply-templates select="../../did/unittitle"/><xsl:text>|TRUE|</xsl:text>
                </xsl:when>
                
                <xsl:otherwise>
                    <xsl:text>[No Title Given]</xsl:text><xsl:text>|TRUE|</xsl:text>
                </xsl:otherwise>
            </xsl:choose>

            <!-- Add service copy -->
            <xsl:choose>
                <xsl:when test="daoloc[1]/@label = 'full'">
                    <xsl:value-of select="daoloc[1]/@href"/><xsl:text>|TRUE|</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="daoloc[2]/@href"/><xsl:text>|TRUE|</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
            
            <!-- Add thumbnail -->
            <xsl:choose>
                <xsl:when test="daoloc[1]/@label = 'thumb'">
                    <xsl:value-of select="daoloc[1]/@href"/><xsl:text>|TRUE|</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="daoloc[2]/@href"/><xsl:text>|TRUE|</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
            
            <!-- EOF -->
            <xsl:text>$</xsl:text>
            
        </xsl:for-each>
    </xsl:template>
    
</xsl:stylesheet>