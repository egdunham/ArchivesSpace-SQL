<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:template match="dsc">

            

            <!-- If c01 is a series, route -->

                
                <xsl:for-each-group select="." group-by="@level">
                    <xsl:value-of select="."/>
                    <xsl:for-each select="current-group()">
                        <xsl:if test="*[@level='series']">
                            <xsl:value-of select="."/>
                        </xsl:if>
                        
                        
                    </xsl:for-each>

                        
                    
                </xsl:for-each-group>
                
            
            
            
            <!-- Otherwise, call CSV item template -->

        
        
    </xsl:template>
    
    <xsl:template name="subseries">
        <xsl:param name="series" />
        <xsl:value-of select="$series"/>
        
        <!-- KEEP LOOPING UNTIL YOU HIT FILE -->
        
    </xsl:template>
    
    <xsl:template name="generate_subseries_name">
        
    </xsl:template>
    
    
    
    <!-- NEED REGULAR CONTAINER LIST -->
    
</xsl:stylesheet>