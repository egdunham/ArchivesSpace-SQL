<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    
    
    <xsl:template match="node() | @*">
        

            <xsl:copy>
                <xsl:apply-templates select="node() | @*"/>
                <!-- <xsl:call-template name="control_access_formatting"/> -->
            </xsl:copy>
        

    </xsl:template>
    <!-- Remove all <daogrp> tags regardless of location -->
    
    <!-- NOTE: Reconfigure to remove the whole <c0#> in cases where title is inherited from parent -->
    
    <xsl:template match="//daogrp"/>

</xsl:stylesheet>