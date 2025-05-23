PGDMP  ;                    }            test_db    17.3    17.3 E    #           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            $           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            %           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            &           1262    26162    test_db    DATABASE     m   CREATE DATABASE test_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'ru-RU';
    DROP DATABASE test_db;
                     postgres    false            �            1255    26163    calculate_order_item_total()    FUNCTION     �   CREATE FUNCTION public.calculate_order_item_total() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.total_price = NEW.unit_price * NEW.quantity;
    RETURN NEW;
END;
$$;
 3   DROP FUNCTION public.calculate_order_item_total();
       public               postgres    false            �            1255    26164    update_products_updated_at()    FUNCTION     �   CREATE FUNCTION public.update_products_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP; -- Устанавливаем текущее время
    RETURN NEW;
END;
$$;
 3   DROP FUNCTION public.update_products_updated_at();
       public               postgres    false            �            1255    26165    update_stock_quantity()    FUNCTION     P  CREATE FUNCTION public.update_stock_quantity() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    DECLARE
        item RECORD;
    BEGIN
        -- Проходим по всем позициям заказа и обновляем запасы на складе
        FOR item IN (SELECT product_id, quantity FROM order_items WHERE order_id = NEW.order_id)
        LOOP
            -- Обновляем существующие записи в stock
            UPDATE stock 
            SET quantity = quantity + item.quantity,
                last_restocked = CURRENT_DATE,
                updated_at = CURRENT_TIMESTAMP
            WHERE product_id = item.product_id AND 
                  warehouse_id = (SELECT warehouse_id FROM stock WHERE product_id = item.product_id LIMIT 1);
            
            -- Если товар не найден ни на одном складе, добавляем его на первый склад
            IF NOT FOUND THEN
                INSERT INTO stock (product_id, warehouse_id, quantity, last_restocked)
                VALUES (item.product_id, 
                        (SELECT warehouse_id FROM warehouses ORDER BY warehouse_id LIMIT 1), 
                        item.quantity, 
                        CURRENT_DATE);
            END IF;
        END LOOP;
        
        RETURN NEW;
    END;
    $$;
 .   DROP FUNCTION public.update_stock_quantity();
       public               postgres    false            �            1259    26166    order_items    TABLE     J  CREATE TABLE public.order_items (
    order_item_id integer NOT NULL,
    order_id integer,
    product_id integer,
    quantity integer NOT NULL,
    unit_price numeric NOT NULL,
    total_price numeric NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT order_items_quantity_check CHECK ((quantity > 0)),
    CONSTRAINT order_items_total_price_check CHECK ((total_price > (0)::numeric)),
    CONSTRAINT order_items_unit_price_check CHECK ((unit_price > (0)::numeric))
);
    DROP TABLE public.order_items;
       public         heap r       postgres    false            �            1259    26176    order_items_order_item_id_seq    SEQUENCE     �   CREATE SEQUENCE public.order_items_order_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.order_items_order_item_id_seq;
       public               postgres    false    219            '           0    0    order_items_order_item_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.order_items_order_item_id_seq OWNED BY public.order_items.order_item_id;
          public               postgres    false    220            �            1259    26177    orders    TABLE       CREATE TABLE public.orders (
    order_id integer NOT NULL,
    order_date date NOT NULL,
    supplier_id integer,
    total_amount numeric NOT NULL,
    status text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT orders_status_check CHECK ((status = ANY (ARRAY['в обработке'::text, 'доставлен'::text, 'отменен'::text]))),
    CONSTRAINT orders_total_amount_check CHECK ((total_amount > (0)::numeric))
);
    DROP TABLE public.orders;
       public         heap r       postgres    false            �            1259    26186    orders_order_id_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.orders_order_id_seq;
       public               postgres    false    221            (           0    0    orders_order_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;
          public               postgres    false    222            �            1259    26187    products    TABLE       CREATE TABLE public.products (
    product_id integer NOT NULL,
    product_name text NOT NULL,
    product_description text,
    category text,
    unit_price numeric NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT products_category_check CHECK ((category = ANY (ARRAY['электроника'::text, 'одежда'::text, 'обувь'::text, 'мебель'::text, 'товары для спорта'::text, 'инструменты'::text, 'бытовая техника'::text, 'здоровье'::text, 'товары для дома'::text, 'продукты'::text]))),
    CONSTRAINT products_unit_price_check CHECK ((unit_price > (0)::numeric))
);
    DROP TABLE public.products;
       public         heap r       postgres    false            �            1259    26196    products_product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.products_product_id_seq;
       public               postgres    false    223            )           0    0    products_product_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.products_product_id_seq OWNED BY public.products.product_id;
          public               postgres    false    224            �            1259    26197    stock    TABLE     p  CREATE TABLE public.stock (
    stock_id integer NOT NULL,
    product_id integer,
    warehouse_id integer,
    quantity integer NOT NULL,
    last_restocked date,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT stock_quantity_check CHECK ((quantity >= 0))
);
    DROP TABLE public.stock;
       public         heap r       postgres    false            �            1259    26203    stock_stock_id_seq    SEQUENCE     �   CREATE SEQUENCE public.stock_stock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.stock_stock_id_seq;
       public               postgres    false    225            *           0    0    stock_stock_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.stock_stock_id_seq OWNED BY public.stock.stock_id;
          public               postgres    false    226            �            1259    26204 	   suppliers    TABLE     L  CREATE TABLE public.suppliers (
    supplier_id integer NOT NULL,
    supplier_name text NOT NULL,
    contact_person text,
    phone_number text,
    email text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT suppliers_email_check CHECK ((email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'::text)),
    CONSTRAINT suppliers_phone_number_check CHECK ((phone_number ~ '^\d{11}$'::text)),
    CONSTRAINT suppliers_phone_number_not_null CHECK ((phone_number IS NOT NULL))
);
    DROP TABLE public.suppliers;
       public         heap r       postgres    false            �            1259    26214    suppliers_supplier_id_seq    SEQUENCE     �   CREATE SEQUENCE public.suppliers_supplier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.suppliers_supplier_id_seq;
       public               postgres    false    227            +           0    0    suppliers_supplier_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.suppliers_supplier_id_seq OWNED BY public.suppliers.supplier_id;
          public               postgres    false    228            �            1259    26215    users    TABLE     `  CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    full_name character varying(100) NOT NULL,
    is_admin boolean DEFAULT false,
    email character varying(100) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.users;
       public         heap r       postgres    false            �            1259    26222    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public               postgres    false    229            ,           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public               postgres    false    230            �            1259    26223 
   warehouses    TABLE     p  CREATE TABLE public.warehouses (
    warehouse_id integer NOT NULL,
    warehouse_name text NOT NULL,
    location text NOT NULL,
    capacity integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT warehouses_capacity_check CHECK ((capacity > 0))
);
    DROP TABLE public.warehouses;
       public         heap r       postgres    false            �            1259    26231    warehouses_warehouse_id_seq    SEQUENCE     �   CREATE SEQUENCE public.warehouses_warehouse_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.warehouses_warehouse_id_seq;
       public               postgres    false    231            -           0    0    warehouses_warehouse_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.warehouses_warehouse_id_seq OWNED BY public.warehouses.warehouse_id;
          public               postgres    false    232            D           2604    26232    order_items order_item_id    DEFAULT     �   ALTER TABLE ONLY public.order_items ALTER COLUMN order_item_id SET DEFAULT nextval('public.order_items_order_item_id_seq'::regclass);
 H   ALTER TABLE public.order_items ALTER COLUMN order_item_id DROP DEFAULT;
       public               postgres    false    220    219            G           2604    26233    orders order_id    DEFAULT     r   ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);
 >   ALTER TABLE public.orders ALTER COLUMN order_id DROP DEFAULT;
       public               postgres    false    222    221            J           2604    26234    products product_id    DEFAULT     z   ALTER TABLE ONLY public.products ALTER COLUMN product_id SET DEFAULT nextval('public.products_product_id_seq'::regclass);
 B   ALTER TABLE public.products ALTER COLUMN product_id DROP DEFAULT;
       public               postgres    false    224    223            M           2604    26235    stock stock_id    DEFAULT     p   ALTER TABLE ONLY public.stock ALTER COLUMN stock_id SET DEFAULT nextval('public.stock_stock_id_seq'::regclass);
 =   ALTER TABLE public.stock ALTER COLUMN stock_id DROP DEFAULT;
       public               postgres    false    226    225            P           2604    26236    suppliers supplier_id    DEFAULT     ~   ALTER TABLE ONLY public.suppliers ALTER COLUMN supplier_id SET DEFAULT nextval('public.suppliers_supplier_id_seq'::regclass);
 D   ALTER TABLE public.suppliers ALTER COLUMN supplier_id DROP DEFAULT;
       public               postgres    false    228    227            S           2604    26237    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public               postgres    false    230    229            V           2604    26238    warehouses warehouse_id    DEFAULT     �   ALTER TABLE ONLY public.warehouses ALTER COLUMN warehouse_id SET DEFAULT nextval('public.warehouses_warehouse_id_seq'::regclass);
 F   ALTER TABLE public.warehouses ALTER COLUMN warehouse_id DROP DEFAULT;
       public               postgres    false    232    231                      0    26166    order_items 
   TABLE DATA           �   COPY public.order_items (order_item_id, order_id, product_id, quantity, unit_price, total_price, created_at, updated_at) FROM stdin;
    public               postgres    false    219   5b                 0    26177    orders 
   TABLE DATA           q   COPY public.orders (order_id, order_date, supplier_id, total_amount, status, created_at, updated_at) FROM stdin;
    public               postgres    false    221   �g                 0    26187    products 
   TABLE DATA              COPY public.products (product_id, product_name, product_description, category, unit_price, created_at, updated_at) FROM stdin;
    public               postgres    false    223   �j                 0    26197    stock 
   TABLE DATA           u   COPY public.stock (stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at) FROM stdin;
    public               postgres    false    225   Ly                 0    26204 	   suppliers 
   TABLE DATA           |   COPY public.suppliers (supplier_id, supplier_name, contact_person, phone_number, email, created_at, updated_at) FROM stdin;
    public               postgres    false    227   B|                 0    26215    users 
   TABLE DATA           i   COPY public.users (user_id, username, password_hash, full_name, is_admin, email, created_at) FROM stdin;
    public               postgres    false    229   ��                 0    26223 
   warehouses 
   TABLE DATA           n   COPY public.warehouses (warehouse_id, warehouse_name, location, capacity, created_at, updated_at) FROM stdin;
    public               postgres    false    231   8�       .           0    0    order_items_order_item_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.order_items_order_item_id_seq', 157, true);
          public               postgres    false    220            /           0    0    orders_order_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.orders_order_id_seq', 61, true);
          public               postgres    false    222            0           0    0    products_product_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.products_product_id_seq', 101, true);
          public               postgres    false    224            1           0    0    stock_stock_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.stock_stock_id_seq', 604, true);
          public               postgres    false    226            2           0    0    suppliers_supplier_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.suppliers_supplier_id_seq', 51, false);
          public               postgres    false    228            3           0    0    users_user_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.users_user_id_seq', 2, true);
          public               postgres    false    230            4           0    0    warehouses_warehouse_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.warehouses_warehouse_id_seq', 31, true);
          public               postgres    false    232            f           2606    26240    order_items order_items_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (order_item_id);
 F   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_pkey;
       public                 postgres    false    219            h           2606    26242    orders orders_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public                 postgres    false    221            j           2606    26244    products products_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public                 postgres    false    223            n           2606    26246    stock stock_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_pkey PRIMARY KEY (stock_id);
 :   ALTER TABLE ONLY public.stock DROP CONSTRAINT stock_pkey;
       public                 postgres    false    225            p           2606    26248    suppliers suppliers_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (supplier_id);
 B   ALTER TABLE ONLY public.suppliers DROP CONSTRAINT suppliers_pkey;
       public                 postgres    false    227            r           2606    26250    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public                 postgres    false    229            t           2606    26252    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    229            v           2606    26254    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public                 postgres    false    229            x           2606    26256    warehouses warehouses_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.warehouses
    ADD CONSTRAINT warehouses_pkey PRIMARY KEY (warehouse_id);
 D   ALTER TABLE ONLY public.warehouses DROP CONSTRAINT warehouses_pkey;
       public                 postgres    false    231            k           1259    26257    idx_stock_product_id    INDEX     L   CREATE INDEX idx_stock_product_id ON public.stock USING btree (product_id);
 (   DROP INDEX public.idx_stock_product_id;
       public                 postgres    false    225            l           1259    26258    idx_stock_warehouse_id    INDEX     P   CREATE INDEX idx_stock_warehouse_id ON public.stock USING btree (warehouse_id);
 *   DROP INDEX public.idx_stock_warehouse_id;
       public                 postgres    false    225                       2618    26259    stock delete_negative_stock    RULE     �   CREATE RULE delete_negative_stock AS
    ON UPDATE TO public.stock
   WHERE (new.quantity <= 0) DO INSTEAD  DELETE FROM public.stock
  WHERE (stock.stock_id = new.stock_id);
 1   DROP RULE delete_negative_stock ON public.stock;
       public               postgres    false    225    225    225    225                       2620    33608    orders after_order_delivered    TRIGGER     �   CREATE TRIGGER after_order_delivered AFTER UPDATE ON public.orders FOR EACH ROW WHEN (((new.status = 'доставлен'::text) AND (old.status = 'в обработке'::text))) EXECUTE FUNCTION public.update_stock_quantity();
 5   DROP TRIGGER after_order_delivered ON public.orders;
       public               postgres    false    221    246    221            ~           2620    26261 $   order_items before_order_item_insert    TRIGGER     �   CREATE TRIGGER before_order_item_insert BEFORE INSERT ON public.order_items FOR EACH ROW EXECUTE FUNCTION public.calculate_order_item_total();
 =   DROP TRIGGER before_order_item_insert ON public.order_items;
       public               postgres    false    233    219            �           2620    26262     products products_update_trigger    TRIGGER     �   CREATE TRIGGER products_update_trigger BEFORE UPDATE ON public.products FOR EACH ROW EXECUTE FUNCTION public.update_products_updated_at();
 9   DROP TRIGGER products_update_trigger ON public.products;
       public               postgres    false    234    223            y           2606    26263 %   order_items order_items_order_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;
 O   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_order_id_fkey;
       public               postgres    false    221    4712    219            z           2606    26268 '   order_items order_items_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id) ON DELETE CASCADE;
 Q   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_product_id_fkey;
       public               postgres    false    223    4714    219            {           2606    26273    orders orders_supplier_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(supplier_id) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_supplier_id_fkey;
       public               postgres    false    4720    221    227            |           2606    26278    stock stock_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id) ON DELETE CASCADE;
 E   ALTER TABLE ONLY public.stock DROP CONSTRAINT stock_product_id_fkey;
       public               postgres    false    4714    225    223            }           2606    26283    stock stock_warehouse_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_warehouse_id_fkey FOREIGN KEY (warehouse_id) REFERENCES public.warehouses(warehouse_id) ON DELETE CASCADE;
 G   ALTER TABLE ONLY public.stock DROP CONSTRAINT stock_warehouse_id_fkey;
       public               postgres    false    225    231    4728               q  x��[Ar1;˯��%Q����ɬ�C�C�L'�m8��H,,*E{�E�3���զ�u|K�����hrSD�í�h+���/�i�Q�mv���-�p ⶌt]��V�HF�ů���w�/�G]wk[l}�uk�f�<s]�{$��O��������
�k������!���Ð��2��Zֵ�n�".��a����u��]f�������VV���+NT���,�%2���>�x��]�R�׃�H3�"���z�m��u=�H�A��n���3�'�췗ٽ ���$9 �({#����vq_'py1w&g��q0�����}�(͗�Q>Ҷ�+���P{��-�Br�uQ:���se�$$�S�ɬ\�9����x����f�rx��,�ONYTa6*O^�	��¢Ձ�^;@o��"��v�ɣ�b~���8d�n���ڹ��%�m�t{�&��J�u`Ҽ��շ�`��)�X<������������-R�LO?���1�\��^?)O8�O������Ƀ���z�c̾�F��B�s�ѻ<~�����p�H��V�q1�>�8����Q�?����&6��NC�$�^p�z";� (1�G<���I-�!�c`�����zA�09��j�I�y�q�zy3�K���k*��oy�ta�y��!�-�!��g4"��g24��l�T0���FuEwy�cvּ�+�Ij�R���\OW
p��׼s���J�2O�J�������$"rf�?��	�`�Ř!4&M��
�&�|�V`Ħe�T���Z�f�a+�&���
�W�+�#bh�VP��B+�E��
� ���V�L�e��|��B+Pf��S+`r����N��� <�����m�R�V���R�f�O;�pC!�;xܶC(XL�N��Hm:�u"*-t��H�f�,%���#�m��	�K��6��,�<N.-���O,��A�6�`W"��}u���HjH�1߸��
 &�I�ƿ3��>�`��ћT��(�qٙڝ������0'
��.�Z�M�L�[�^ИǮ�� t"��`��j���Μ ��1 )Ma "B)���D�K���T0�|��D�K��6&@s.�L}Y�m��/�i7Ho ��70*>�p�y��ui9XL�Z~<\,����$�4���R�s(����L���L�K�S����`R��y@�g�dR]::SI��X��34��ԉ%�ʜZ%��q#�ԗ����Me���{xIUٕ� 󵕤���҄���I*�Huٵf���%�։]B�7?~��ɗأ�C�}�50�����m��O��ψ�Q�}�N���[n�
Kj������x�ˆ��ǐ��nK?ܺ���n���UJ�         	  x��X�q�0����NC� �%�$�(��?y��#/D���8�����+�b	�(pd��t%����c��O�ߞ������k���/�~�r��Ųi][������'_)�Zmt <\�����+ �v���?	�N�r)�֚�kr"�A���@�'�m��#���qNBD��7K�&6׀�h����f�w��Ml�,�f-�&E�	�VBP����d>8��W��4��F�ZTojxE�����~*�K�dl` ���Tw[)�U��)��2�+��U���U�`��ܩ�,�һ*�Q5��kW��R5<n��ݯ[>�� ]uu�����Uم�k@&���������s��>w�*7�N��/U��û���i���r�&�U���r��ė�ar�z��ݩ�f��	��T�ap�O��}��������J��0�E�u�i�#���V�/U�Ɂ!��ĝ�i�F{W%?��A���Xp��nTMS�_�rO�[_�}��h�W�Γ��2�mĢ�:�dZ���{~�KD���1�6�4f��]����ĸC���Q>����%�Mq�+����8�kg��o�a��n���B#C�9�~M;��_�D�/	2��h3�#U�z�d�����ū��w�^�(�h����Սx��rN-�w�MSw(6d?a{^�i�L�ߎf��	��T��qZ��\�&�&i�,�F��-Ҧ��X� D�V�[I��n	WOə�[�b]�i�%�th�{l��;��<`$n��\A|���L�W�ę�/�,/�         m  x��[Ys��~ŝ<��$� �Q�b{bIQ^&�XFm�(2�b�o�9cǪ�<�i�$�C;��@$aQ�4���/����s/H�$*д�D���p?��;�T���3v�}��=p��X�Wb���j˵ڶ����Iv��4+�F�n��.�_:�v�댝��s��%�Z�PH˲�ʪ��3)Uc�����l��甜v���&9�u:�Ķc��
w����}�>�/JM�Y�U�.9'��N�m;������(|�B,|:J�I�O�R���=��RdY~�
�y"����m���Q��x����'��.�ς�9r_;g�c��ǀ��b�Fm�ς����{t��)/�����:{\{O˕����]���t(4=F�]�`��`�@��kxO��O�}9��3���|O������z�h<l�լ��[��ٔ����!����Ul0�݃��Y�!���Ȓ��$�y��ħ�LIz�N �t,v�E�V���)��N�	��Z<ST��g�����4eT$@4"#=��P8}�،\���n�/���"����%�	%�Wd:�{K*�I���!|��}N�s1�|L왠�{��">A����pe����QI-KY�a�����~�Got&�-!��xm[��!���,x�7]�K$f�̀��M	��c��%��x�>�*#W;A��ap�x�� �G�S(�û)���/.�L�0	�吸�"��f�EkjH�x{T=�����:&�*@��c䣓�R����X�I�+��:�Ss�J2cAgX>���|M>!��1�1Ix@�$���!Q�1:P�)`��c��x����[��ҽ`t��P-�i�ޡ8|���W��Qӊ��c�7fi��@_�Hѥ��!^}�5L�?�6�´�}�"���!V(���꺯�0�O�y�e@�~�b�J,�*���l��S:�d�4Z�'L�H�uH+K;F��6�Gf��R���-�]A��yo�;�d���yT6@���&��C2��	9��|d�%��V5=�)\J�*�k�2���Q���6�hL6 x	w��<=��><�������������]^R��g ��Ov@> �����[����_�����W�j�I�8����8H��n<5�f�g}}��3��\#�Ȕg���;$A*%6k;l�(Wj�HU�h:�@9{3̗xZ��7�ʡdz��pR�-��U6���tE�M�Z?Pr `�$��!nU�G:�}�-�kͦ��`�ͪ�4�&tfB�/).�BЂ����eb� ��$�L��#�dN(���CF:��z������5�$:� (��#-&��jEe�M@����Q��2ܥ��� f�s/��[gȖ���Y_�fa�u�/1�df�R����M�gk����F��f�4)C�tr���c�C�]�g3�	OSF4C���7n������"ի���0&��\��f�^S���Jͺ�U��X�o�xJ�0ۺ�H��%�Y�&[�[��d�U�<�#m�S��zܽ�ʮ���3��P|���븡�@8��k�M��m,� ��6����4�0��9#�6#��5�Ӏr�F�![n���F�f�.Q��0Pw�I�"��/>k�����:����Ɋ�:[5>�	�����څ9ʓ5y)�K+9�g.����������(m)�*F�1O����erj�+/|j�?U3���\�����`�v�U��p��,�p�X��`^���ZY�ݬ�h���?�~�Cg��!�a�/>.?6�^�Y7�jp
�L���\�>��#����5�����Ɲ�[�s�5���庌17o����Ym4kH��B�l�K&jy��b
'΅!��F�r��:�7:rj�iE@C��� B��|�y�Q��4"�	��4�M�E�`�<C+����Y��צ& f@Ply��[W��cO4����GW�����u�O����d�귏�"fB�+��z�۾HϺ�k�@���i�*O�>��T�v�xn�/�ӳ�F�,���4Z
�%��jKz6�f�BNM�Z�e	O=ħ�Y�0�wE�����3Ϝ��wIF��+����ja� &`�/躜K�0C���֎!ќ�c��\�z��ϛ�C��Y��h/��Y��n��m��Ө4����4�a��j@���+^���t��S��,������б~Hdv|��Sc�ƙ�8g���sb�0oŭ�	�K�q��������ݻ�p����q����E�1ϝ��O̼#<�����h��хW7+�f<+?1��zJ���ʂ�0^S��<����gK�D@�* kdr�DߥD��k1�IN���ޑ�FNɂD�c~�y)�.
8�;��=�<���}����AON�K�Ŕ��N��;���f{|t`� �i-�xA���}�̸yDna�:�h��?�VM�'� T�d�r~w9Έ���qҴ�}bl�����fc*�����Iӝ�]�;���d�IT6}K4���\r3���	�����ҧF�q��$hչ$oT���(T.}����o�G���4�DV��0e��*�^�#b�* �����[��I�:�j>:M�킎h��@�|?k�r�QAjA�9�7���������U2Bq.������TR �
#W���M��!��$z�|FCk
�P?��,e�4�M=?;M�_JTN�#j�c�>v����3�^5hn�~����-S�:��Wؾ���� ����]�jF����,���$<Y]��]A��Cn#QkC7�F��yZ���6`���}�(t�Ŀ0:P��<��>�3����E���dSˣ�v��C��rcalY����E0o?h�f_-W��m�D�m���48E�PTN�0�my�m	�`SuA40r$\y��.���)�E�L��1?���"����a9�FP�Ю=]�B+�0ꐏE~L�k�<c"-���閶<�n"�Sj1��PLl��1[$W���X��v���(X~ӏvL��D�4�ST����e&�~��I��Qo���(�.�#�Ba��5�YPqʧF8�P�2JpH(��Q����.��?-+�})�UqgE0`�#����p���~�h�)�fڠͥ  5L�W �unH'�@m�v|�,�N#o�1�y7�;2��B��+��H^�y�:�b�db�y��I�Ŭ+ ���X$���' nF���ĝ�cʚ�fa���7�����s��T��:]���RW ��[1=�oPL:���p����0ߘ����kSov�"*9��5�w�ǋR����5#��]�+�(`:���(���2�H�3�d"��Jr<����hu�¶	b��q��ӈ�((��ك����7Yf�%*���MgBm�"@ c�<��r�,�� ���?�wjn�X�!��I�!@q������{���{̔z�̘g<o�i!�y�$��4j�6�,�G��P(�}am>���p�Zb�Ȅ��6pы�$){�5�œ\���s�&d�-H�4�^_o>��@��Q�{J����'��8�+=���}��ru��Z1/+/�O�k��W�Ï�"P6ۨ=��k[۬���َ�T��o7.��}щ_إ��͎yn��lը7�jCR���� ���42��0P!3>�-i�+��嵜�'~�N$��$         �  x���I��0E��)�6�I�Yr�s�S���@q"ŨZ�!�8}�ͅ�c1pdݣ�������C�5�CX����Mů�(s�@�	#����wXb������%;�R��b9�"ez8�D�@�
,E	%T��>���C�L�ؑ,k�G`)X��U[LM�`�FOG`��`��[Tn��F�i9��؟�4q�,��TC��$�����e���#s��717�q;Z��{,�Tk���0�y����]��A����h�D�{��LX�v6/�/NҦK\r /�t����ƥ�l���Q����&Z����Cش�2��!�3�~5M�E7��4��?��0���0�M�c/O�5�4�Ҍ;-�Bs�B�/%��
~�m��L���T��Q�jòZT�BQB�f��S��坟~�1o�f�e����wN�	���0�8�ށ� ��5�,뭨�lȚ�X)n`�������B+��]�(BJ7}\nx%�y�ߡA00u��r���04�z�����7Ȣ��K4X
�e����Q�h�a�ʍy�^��t�S	��G�,^�̣��W`Р���]��N�j��@4�M�3&_� �2����0���Xo��4�6��'[�]�n~��W��V��K4�}נo��z����_¦��.UPVծ,�`�G�i3��n㲭�j`8��o���ష35�&�B�|^Ρ�}����K{_�ޠ	Ƙ��VZ���4���Ú2��w��G����~�Ƕm?��,         ;  x��X]S�F}^~���x�,Y2O䋦S2��}�b��Y�d7�����)�0e���/�p�` a��z���!�0��JG�{���ɬ.��0��x���N����`u�_�#�!���a�f�DjrA3`3ˎ_�O
A��S�99U�ԋ9͚6�i�*��^����h�H���s~����S��x�w��`~���-�����XFٴ,˶�e�ʢ�~d�W�i8��� �U@�?��(x����?�=~�/2hz�0K��
V�xn}��M|ޣ�*�b������d��l��w@Aw��%e�*�F�8��5� 
I(~��=߆�g�C\�U�w�)�هR �=�^_BN$%6	��-/�FӣK��4,�E��A= K=�'Rv? �u�lE��En�]�"Zw"�$r=�ȎMf�>p�%�	\t MWH 9��:��"+��,m���b)��nݍo�� �e��z���K}�6���-� ��*�>k��&[W��.tq�zp�.m�
[į+kA�jJ}��$ĸ�Z%� !�s� tP�X/.%l�����A#���H�.zr�`=��	�e�ڶ�ʕ4����J�(
<�5<�18�J̍T��C�?@�𳗀"�I�O��C�݊j�h��G�Y�J�JU�ms|C(��T6��)�LC\��ԵR"k5x�9קb���:����>����O���q0�΃u�5��-�廁ۦ�М	�:��-^��j������TKa��-��
#,0��K�ʉY��)�u��&�[��q���ɂt��qb�a��#��}�@�[�N������ob��Sd6��"Z�|���\���B�(֫���x[��ή(]#_/�3�A�
A��t��8��t&�����5n"��:z���v��|�Z�6B�[��������+0%	��W�
3uQ�
k|)�"v��_�Kqn�Y��J������C9��ǎ����Hg��T X�_�y'�U����Lrj@V	\���d83A���A.��!��ubCq��f����� �gB@��S�}�Rbz#G��?��@��V%�C�2"6f��dy �a<=��+��ᩝиh.�C6n�j6����
}:��IY� ʣ)�#k�3�7
}�V�U�T�JRV:�gl��Ծ�/�"�8]��܊�>��@�6��:�$v�m�&��0�L��1eP:yP��J�Ġ���;��n�U���X$����a�i 	�vĶMn�C�l����\�~�G��IHYX c�!�"��&y، �f�n(��&(��b�P�#�1liIc��U��"���q���"g�Ԑ�G�0��k�Gm���$BÓ4��`ƿ�r9�G.���}�p�S�Z���Ȕe��R�(�֘�~���AG{�k���Hl7?rd�9��v��N=`u꫞�iW��cˡ~��9�|f���9f(�Ў����$CO!�'~_�t�$�?��-�)�4�Ê��TL��B��1�B�^�7���D�>�5꩞&��}��~�	p���]�6	�� �_0h�#���-4΍X٢n�Ss�(XV��DJ��u s���;RHyY�U�,�7𳉚��[V����D�u��/P�;q�ލI�m7������
�J�ۃjm "����v@H/��B]���|��<<7U>04�q����Mș���E�v��j}�
��t\���Ix�	ta�է�����`�t3'h�T�>���1I�7�͆���B��W�&����d�x��&���v#�����Ƥ��"~T��U���f�;u�;n�|uD���!�TpuV.k�,M��e5{��������j         �   x�3�LL��̃��FƜ&\�raυ�^�q��b�ņ.6]�w�A��B�Ѕ��\��,�hr(O,J��/-N�+*�4202�50�54T04�24�22�35�43��2��M�KLO-��`�� M��[.l��dɜ.l��`7l�L�)'ڢ=... �G[�         �  x��Wk��0�mN�d;1���P��J[	�j�UՖ�Vm��<�,,��7�g"Lȣ�d<��7�F����h�g:�X.h�OZ�^�����ہӮ�T�@O�F����U�fz��s�$�*�Q(�@�O*��^��I�V+r }�8�#Z���ziɊ62t�X�W�Y_y�\_p�%eCs��1î�k0����)�'<���o���г�9�c;����~ױg�π��0����z̊���&8���-q��f��=̮ !�s���+��7�-�D=��F��U&������;����{�큹�j�]�p����dȧ;_Ԁ��j C:0���P����V�_8�NOL���,����G�T��~e|a�7�A]F$�%>����byU5�Eh�=9U�+�R� �En��[�u�����-�7n��c���Y.�(a9Uy5h�[˾�������2F�ӁKӁ`Njr�(TdM��^���e"���u2��B溎����;K߫�d��c�.ʉ`z�5[v]]+wdnu����^qh��LΩ�S��EUw�!�b�9�aAS[�%q� ���s�o����D��%�%�hU�47 ҃���Ux�.�I�y�Hӭ�������ՙ�B��e��14��7�~�dB�Nu�!%�E�w��^<�״a'�:��F���I�1���S.���M���2_I���晗��-�u�š���Q2�e'ݾ�[/:�V�����     