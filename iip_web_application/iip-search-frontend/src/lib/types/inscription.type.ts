export enum EditionType {
    DIPLOMATIC = "diplomatic",
    TRANSCRIPTION = "transcription",
    TRANSCRIPTION_SEGMENTED = "transcription_segmented",
    TRANSLATION = "translation"
}

export type Edition = {
    edition_type: EditionType;
    raw_xml: string;
    text: string;
}

export type Image = {
    description?: string;
    graphic_url: string;
}

export type Language = {
    label: string;
    short_form: string;
}

export type Inscription = {
    id: number;
    city: any;
    description?: string;
    dimensions?: any;
    editions?: Edition[];
    filename: string;
    images?: Image[];
    languages?: Language[];
    location_coordinates?: number[];
    location_metadata?: any;
    not_after?: string;
    not_before?: string;
    short_description?: string;
    title?: string;
}