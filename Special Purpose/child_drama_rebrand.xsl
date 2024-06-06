<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <!-- Copy everything not affected by the rebrand -->
    
    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*"/>
        </xsl:copy>
        
    </xsl:template>
    
    <xsl:template match="publicationstmt/publisher">

            <xsl:element name="publisher">
                <xsl:attribute name="encodinganalog">publisher</xsl:attribute>
                <xsl:text>Arizona State University Library.  Theatre for Youth and Community Collection.</xsl:text>
            </xsl:element>
        

    </xsl:template>
 
    
    <xsl:template match="repository/corpname">

            <xsl:choose>
                
                <!-- Handle inclusion of subarea -->
                <xsl:when test="subarea">
                    <corpname encodinganalog="852$a">Arizona State University Library 
                        <subarea encodinganalog="852$b">Theatre for Youth and Community Collection</subarea></corpname>
                </xsl:when>
                
                <xsl:otherwise>
                    <corpname encodinganalog="852$a">Arizona State University Library. Theatre for Youth and Community Collection</corpname>
                </xsl:otherwise>
            </xsl:choose>
            
        
    </xsl:template>
    
    <!-- General replace template -->
    
    <xsl:template name="string-replace-all">
        <xsl:param name="text" />
        <xsl:param name="replace" />
        <xsl:param name="by" />
        <xsl:choose>
            <xsl:when test="contains($text, $replace)">
                <xsl:value-of select="substring-before($text,$replace)" />
                <xsl:value-of select="$by" />
                <xsl:call-template name="string-replace-all">
                    <xsl:with-param name="text" select="substring-after($text,$replace)" />
                    <xsl:with-param name="replace" select="$replace" />
                    <xsl:with-param name="by" select="$by" />
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$text" />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
</xsl:stylesheet>