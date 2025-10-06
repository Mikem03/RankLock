import React, { useState, useMemo } from 'react';
import { HeroNameCellRenderer } from './HeroImage';
import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community'; 
import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import { themeQuartz, iconSetQuartzBold } from 'ag-grid-community';
import 'ag-grid-community/styles/ag-theme-quartz.css'; // Optional theme CSS


ModuleRegistry.registerModules([AllCommunityModule]);

const myTheme = themeQuartz
	.withPart(iconSetQuartzBold)
	.withParams({
        backgroundColor: "#1f2836",
        browserColorScheme: "dark",
        chromeBackgroundColor: {
            ref: "foregroundColor",
            mix: 0.07,
            onto: "backgroundColor"
        },
        foregroundColor: "#FFF",
        headerBackgroundColor: "#18181B",
        headerFontSize: 14,
        headerFontWeight: 500,
        oddRowBackgroundColor: "#0F1B2F"
    });

const HeroTable = ({ heroes }) => {
    const colDefs = useMemo(() => [
        { 
          field: "name", 
          headerName: "Hero", 
          cellRenderer: HeroNameCellRenderer 
        },
        { 
          field: "pickrate", 
          headerName: "Pick Rate",
          valueFormatter: (params) => (params.value * 100).toFixed(2) + "%"
        },
        { 
          field: "winrate", 
          headerName: "Win Rate",
          valueFormatter: (params) => (params.value * 100).toFixed(2) + "%"
        }
    ], []);

    return (
        <div style={{ height: 700, width: '35%' }}>
            <AgGridReact
                rowData={heroes}
                columnDefs={colDefs}
                theme={myTheme}
            />
        </div>
    )
}

export default HeroTable;