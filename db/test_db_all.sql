PGDMP                      }            test_db    17.3    17.3 E    !           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            "           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            #           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            $           1262    26031    test_db    DATABASE     m   CREATE DATABASE test_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'ru-RU';
    DROP DATABASE test_db;
                     postgres    false            �            1255    26152    calculate_order_item_total()    FUNCTION     �   CREATE FUNCTION public.calculate_order_item_total() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.total_price = NEW.unit_price * NEW.quantity;
    RETURN NEW;
END;
$$;
 3   DROP FUNCTION public.calculate_order_item_total();
       public               postgres    false            �            1255    26154    update_products_updated_at()    FUNCTION     �   CREATE FUNCTION public.update_products_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP; -- Устанавливаем текущее время
    RETURN NEW;
END;
$$;
 3   DROP FUNCTION public.update_products_updated_at();
       public               postgres    false            �            1255    26150    update_stock_quantity()    FUNCTION     !  CREATE FUNCTION public.update_stock_quantity() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE stock 
    SET quantity = quantity + NEW.quantity,
        last_restocked = CURRENT_DATE,
        updated_at = CURRENT_TIMESTAMP
    WHERE product_id = NEW.product_id AND 
          warehouse_id = (SELECT warehouse_id FROM stock WHERE product_id = NEW.product_id LIMIT 1);
    
    -- If the product doesn't exist in any warehouse yet, add it to the first warehouse
    IF NOT FOUND THEN
        INSERT INTO stock (product_id, warehouse_id, quantity, last_restocked)
        VALUES (NEW.product_id, 
                (SELECT warehouse_id FROM warehouses ORDER BY warehouse_id LIMIT 1), 
                NEW.quantity, 
                CURRENT_DATE);
    END IF;
    
    RETURN NEW;
END;
$$;
 .   DROP FUNCTION public.update_stock_quantity();
       public               postgres    false            �            1259    26112    order_items    TABLE     J  CREATE TABLE public.order_items (
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
       public         heap r       postgres    false            �            1259    26111    order_items_order_item_id_seq    SEQUENCE     �   CREATE SEQUENCE public.order_items_order_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.order_items_order_item_id_seq;
       public               postgres    false    228            %           0    0    order_items_order_item_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.order_items_order_item_id_seq OWNED BY public.order_items.order_item_id;
          public               postgres    false    227            �            1259    26094    orders    TABLE       CREATE TABLE public.orders (
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
       public         heap r       postgres    false            �            1259    26093    orders_order_id_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.orders_order_id_seq;
       public               postgres    false    226            &           0    0    orders_order_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;
          public               postgres    false    225            �            1259    26033    products    TABLE       CREATE TABLE public.products (
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
       public         heap r       postgres    false            �            1259    26032    products_product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.products_product_id_seq;
       public               postgres    false    218            '           0    0    products_product_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.products_product_id_seq OWNED BY public.products.product_id;
          public               postgres    false    217            �            1259    26058    stock    TABLE     p  CREATE TABLE public.stock (
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
       public         heap r       postgres    false            �            1259    26057    stock_stock_id_seq    SEQUENCE     �   CREATE SEQUENCE public.stock_stock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.stock_stock_id_seq;
       public               postgres    false    222            (           0    0    stock_stock_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.stock_stock_id_seq OWNED BY public.stock.stock_id;
          public               postgres    false    221            �            1259    26080 	   suppliers    TABLE     L  CREATE TABLE public.suppliers (
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
       public         heap r       postgres    false            �            1259    26079    suppliers_supplier_id_seq    SEQUENCE     �   CREATE SEQUENCE public.suppliers_supplier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.suppliers_supplier_id_seq;
       public               postgres    false    224            )           0    0    suppliers_supplier_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.suppliers_supplier_id_seq OWNED BY public.suppliers.supplier_id;
          public               postgres    false    223            �            1259    26136    users    TABLE     `  CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    full_name character varying(100) NOT NULL,
    is_admin boolean DEFAULT false,
    email character varying(100) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.users;
       public         heap r       postgres    false            �            1259    26135    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public               postgres    false    230            *           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public               postgres    false    229            �            1259    26046 
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
       public         heap r       postgres    false            �            1259    26045    warehouses_warehouse_id_seq    SEQUENCE     �   CREATE SEQUENCE public.warehouses_warehouse_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.warehouses_warehouse_id_seq;
       public               postgres    false    220            +           0    0    warehouses_warehouse_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.warehouses_warehouse_id_seq OWNED BY public.warehouses.warehouse_id;
          public               postgres    false    219            Q           2604    26115    order_items order_item_id    DEFAULT     �   ALTER TABLE ONLY public.order_items ALTER COLUMN order_item_id SET DEFAULT nextval('public.order_items_order_item_id_seq'::regclass);
 H   ALTER TABLE public.order_items ALTER COLUMN order_item_id DROP DEFAULT;
       public               postgres    false    227    228    228            N           2604    26097    orders order_id    DEFAULT     r   ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);
 >   ALTER TABLE public.orders ALTER COLUMN order_id DROP DEFAULT;
       public               postgres    false    226    225    226            B           2604    26036    products product_id    DEFAULT     z   ALTER TABLE ONLY public.products ALTER COLUMN product_id SET DEFAULT nextval('public.products_product_id_seq'::regclass);
 B   ALTER TABLE public.products ALTER COLUMN product_id DROP DEFAULT;
       public               postgres    false    218    217    218            H           2604    26061    stock stock_id    DEFAULT     p   ALTER TABLE ONLY public.stock ALTER COLUMN stock_id SET DEFAULT nextval('public.stock_stock_id_seq'::regclass);
 =   ALTER TABLE public.stock ALTER COLUMN stock_id DROP DEFAULT;
       public               postgres    false    221    222    222            K           2604    26083    suppliers supplier_id    DEFAULT     ~   ALTER TABLE ONLY public.suppliers ALTER COLUMN supplier_id SET DEFAULT nextval('public.suppliers_supplier_id_seq'::regclass);
 D   ALTER TABLE public.suppliers ALTER COLUMN supplier_id DROP DEFAULT;
       public               postgres    false    223    224    224            T           2604    26139    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public               postgres    false    230    229    230            E           2604    26049    warehouses warehouse_id    DEFAULT     �   ALTER TABLE ONLY public.warehouses ALTER COLUMN warehouse_id SET DEFAULT nextval('public.warehouses_warehouse_id_seq'::regclass);
 F   ALTER TABLE public.warehouses ALTER COLUMN warehouse_id DROP DEFAULT;
       public               postgres    false    219    220    220                      0    26112    order_items 
   TABLE DATA           �   COPY public.order_items (order_item_id, order_id, product_id, quantity, unit_price, total_price, created_at, updated_at) FROM stdin;
    public               postgres    false    228   >`                 0    26094    orders 
   TABLE DATA           q   COPY public.orders (order_id, order_date, supplier_id, total_amount, status, created_at, updated_at) FROM stdin;
    public               postgres    false    226   pe                 0    26033    products 
   TABLE DATA              COPY public.products (product_id, product_name, product_description, category, unit_price, created_at, updated_at) FROM stdin;
    public               postgres    false    218   eh                 0    26058    stock 
   TABLE DATA           u   COPY public.stock (stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at) FROM stdin;
    public               postgres    false    222   �v                 0    26080 	   suppliers 
   TABLE DATA           |   COPY public.suppliers (supplier_id, supplier_name, contact_person, phone_number, email, created_at, updated_at) FROM stdin;
    public               postgres    false    224   �                 0    26136    users 
   TABLE DATA           i   COPY public.users (user_id, username, password_hash, full_name, is_admin, email, created_at) FROM stdin;
    public               postgres    false    230   9�                 0    26046 
   warehouses 
   TABLE DATA           n   COPY public.warehouses (warehouse_id, warehouse_name, location, capacity, created_at, updated_at) FROM stdin;
    public               postgres    false    220   �       ,           0    0    order_items_order_item_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.order_items_order_item_id_seq', 1, false);
          public               postgres    false    227            -           0    0    orders_order_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.orders_order_id_seq', 56, true);
          public               postgres    false    225            .           0    0    products_product_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.products_product_id_seq', 101, false);
          public               postgres    false    217            /           0    0    stock_stock_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.stock_stock_id_seq', 601, true);
          public               postgres    false    221            0           0    0    suppliers_supplier_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.suppliers_supplier_id_seq', 51, false);
          public               postgres    false    223            1           0    0    users_user_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.users_user_id_seq', 2, true);
          public               postgres    false    229            2           0    0    warehouses_warehouse_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.warehouses_warehouse_id_seq', 31, true);
          public               postgres    false    219            p           2606    26124    order_items order_items_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (order_item_id);
 F   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_pkey;
       public                 postgres    false    228            n           2606    26105    orders orders_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public                 postgres    false    226            d           2606    26044    products products_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public                 postgres    false    218            j           2606    26066    stock stock_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_pkey PRIMARY KEY (stock_id);
 :   ALTER TABLE ONLY public.stock DROP CONSTRAINT stock_pkey;
       public                 postgres    false    222            l           2606    26092    suppliers suppliers_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (supplier_id);
 B   ALTER TABLE ONLY public.suppliers DROP CONSTRAINT suppliers_pkey;
       public                 postgres    false    224            r           2606    26149    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public                 postgres    false    230            t           2606    26145    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    230            v           2606    26147    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public                 postgres    false    230            f           2606    26056    warehouses warehouses_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.warehouses
    ADD CONSTRAINT warehouses_pkey PRIMARY KEY (warehouse_id);
 D   ALTER TABLE ONLY public.warehouses DROP CONSTRAINT warehouses_pkey;
       public                 postgres    false    220            g           1259    26077    idx_stock_product_id    INDEX     L   CREATE INDEX idx_stock_product_id ON public.stock USING btree (product_id);
 (   DROP INDEX public.idx_stock_product_id;
       public                 postgres    false    222            h           1259    26078    idx_stock_warehouse_id    INDEX     P   CREATE INDEX idx_stock_warehouse_id ON public.stock USING btree (warehouse_id);
 *   DROP INDEX public.idx_stock_warehouse_id;
       public                 postgres    false    222                       2618    26156    stock delete_negative_stock    RULE     �   CREATE RULE delete_negative_stock AS
    ON UPDATE TO public.stock
   WHERE (new.quantity <= 0) DO INSTEAD  DELETE FROM public.stock
  WHERE (stock.stock_id = new.stock_id);
 1   DROP RULE delete_negative_stock ON public.stock;
       public               postgres    false    222    222    222    222            }           2620    26151    orders after_order_delivered    TRIGGER     �   CREATE TRIGGER after_order_delivered AFTER UPDATE ON public.orders FOR EACH ROW WHEN (((new.status = 'доставлен'::text) AND (old.status = 'в обработке'::text))) EXECUTE FUNCTION public.update_stock_quantity();
 5   DROP TRIGGER after_order_delivered ON public.orders;
       public               postgres    false    231    226    226            ~           2620    26153 $   order_items before_order_item_insert    TRIGGER     �   CREATE TRIGGER before_order_item_insert BEFORE INSERT ON public.order_items FOR EACH ROW EXECUTE FUNCTION public.calculate_order_item_total();
 =   DROP TRIGGER before_order_item_insert ON public.order_items;
       public               postgres    false    228    232            |           2620    26155     products products_update_trigger    TRIGGER     �   CREATE TRIGGER products_update_trigger BEFORE UPDATE ON public.products FOR EACH ROW EXECUTE FUNCTION public.update_products_updated_at();
 9   DROP TRIGGER products_update_trigger ON public.products;
       public               postgres    false    233    218            z           2606    26125 %   order_items order_items_order_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;
 O   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_order_id_fkey;
       public               postgres    false    228    226    4718            {           2606    26130 '   order_items order_items_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id) ON DELETE CASCADE;
 Q   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_product_id_fkey;
       public               postgres    false    4708    218    228            y           2606    26106    orders orders_supplier_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(supplier_id) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_supplier_id_fkey;
       public               postgres    false    226    4716    224            w           2606    26067    stock stock_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id) ON DELETE CASCADE;
 E   ALTER TABLE ONLY public.stock DROP CONSTRAINT stock_product_id_fkey;
       public               postgres    false    4708    218    222            x           2606    26072    stock stock_warehouse_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_warehouse_id_fkey FOREIGN KEY (warehouse_id) REFERENCES public.warehouses(warehouse_id) ON DELETE CASCADE;
 G   ALTER TABLE ONLY public.stock DROP CONSTRAINT stock_warehouse_id_fkey;
       public               postgres    false    222    4710    220               "  x��ZK�#K\�O1h+�?>˻�9^ ]e�za�5��iDA �Ȕ2{9E�U}���j�?u�H�'�5۫�s,�?�z�leο�r^�^�>��Z�_�`w�������E��"a�{N��ڰs���~j;�����T~�33��;s�,��>~���38J+��e�Z�79K/#L^����UFY8t-�r���ō�E68;?"��>e�x�;���j�eL8�.;�-	�,��#r��$,ޥ�����3qc����kr&�������7��NX�v@m����Gp�^V���̛Lp �Q�A��#8-aq����;��&QV���)�d^����#��}�;�������Y��c���Qc���+:��N�rQ�����֭<��w�YI/��[���?�1Se��Ѩܼ6�_��2��3w@o��"��#wN�U��VQ+�z׈$�7�p�����g�-Q���-p��u`R�����I`E~J%&O�G#b�h#�>��"�wxz�"*���|��V)3���@��x�d"�:09��1f?��D�.��c0z��c�g�x��!b ��ZA��'wp��D���������R֤O�ǻ'��@�)�8�!.�'�|�L���3�d5��g	�<�`rY��ޓ�9�98B����j�����im�5�<T�0b<N�д#�$Bhz�ш�6���&Fۥ����5�ۻ˫�i�y��4&�M�
�"�z�R�:���N��eJ�dV��J����Y��""rE�?��q�`+��X.4&M.�
�!�|�V�Ħe�T07�۵�ìa;�&�o�
��;�%bh�VP��]+�M��v� �����0Lĥ�¼�خLf�zB+`r�q���N��q� <��q�����R�V����R�a�OǅpC.�;x�v\(�L�N0���u�DT��!���M]'ؓK�Gfۦ�(��B�"��x�<\��9���Hm�:��D�}�_��@$ե�՘7�յ���nR�����_�M<+x�&�8��J5\v�v'��+�w��T�.�X�~�·�zAc�]��׉h(���T�%.
;s�{ǀ�X2�""�\;@�$r\,�C���Md��5��	И�S_��6����X7�� @c�@�����kD�����Ԯ�w瀋%��d�],���Rl�P �w�Բ��0�.6�J����L��7���Ń��T����H�h���5��ԉ%�&sj��>���}@���X?8T���������@�*�+ʼ���Ah�d�XB�̭�-d��0��m�,Z�u���������         �  x��X�q�0����NC� )��������ty!�"�猃L���%�����ӕ4PH�j�s�a����n�ۏ�y���l�I�'Y.��XV]�#1�9��@�+��Aj]*�ϗ�u{�}���_��A�BW�!�\kr-C�i�`<i�������]��8� !"
�ٛ�|��K@`4��]N�YCA;�]��=��ZK�IQO��J
�/�$����"�;MD��hY��S�hp6���O�}��Dr��IUw��"Mu����o+C���]��m]��X�;U��SZWE?�w#����Tu��ar�떻ϣ5@S]ݨ�npt�Ev����ɭ��>j���`�����������KU7���&��y��h������B�`p���eT񥪛�>&gw��Yn{®�#U���ap_�nr  ��v��R�9LnQr��i�ȟ�=���K�`r`H�*q�j���Uɏ�a�#��#�UÔ�ҮuG��	���-��k4�+c��]n��6bQuM2����-��%"�~i~�H�3��.Mn��U��!VEj(_R����8ՙH�R'8�kc��g�n��f���B#]�9�~M��˿`�v_��!�QGG����6`��ۋW)*C��K���V�7(�UhM�Qɹ�e�Ѳ��Qf�?r�T�i2�6�>q�=l��W�3�Tc�s4i�P�����i�L�޿F��B�L*�r?-�JV� G�UҬY��;Gӷy��7�M�         m  x��[Ys��~ŝ<��$� �Q�b{bIQ^&�XFm�(2�b�o�9cǪ�<�i�$�C;��@$aQ�4���/����s/H�$*д�D���p?��;�T���3v�}��=p��X�Wb���j˵ڶ����Iv��4+�F�n��.�_:�v�댝��s��%�Z�PH˲�ʪ��3)Uc�����l��甜v���&9�u:�Ķc��
w����}�>�/JM�Y�U�.9'��N�m;������(|�B,|:J�I�O�R���=��RdY~�
�y"����m���Q��x����'��.�ς�9r_;g�c��ǀ��b�Fm�ς����{t��)/�����:{\{O˕����]���t(4=F�]�`��`�@��kxO��O�}9��3���|O������z�h<l�լ��[��ٔ����!����Ul0�݃��Y�!���Ȓ��$�y��ħ�LIz�N �t,v�E�V���)��N�	��Z<ST��g�����4eT$@4"#=��P8}�،\���n�/���"����%�	%�Wd:�{K*�I���!|��}N�s1�|L왠�{��">A����pe����QI-KY�a�����~�Got&�-!��xm[��!���,x�7]�K$f�̀��M	��c��%��x�>�*#W;A��ap�x�� �G�S(�û)���/.�L�0	�吸�"��f�EkjH�x{T=�����:&�*@��c䣓�R����X�I�+��:�Ss�J2cAgX>���|M>!��1�1Ix@�$���!Q�1:P�)`��c��x����[��ҽ`t��P-�i�ޡ8|���W��Qӊ��c�7fi��@_�Hѥ��!^}�5L�?�6�´�}�"���!V(���꺯�0�O�y�e@�~�b�J,�*���l��S:�d�4Z�'L�H�uH+K;F��6�Gf��R���-�]A��yo�;�d���yT6@���&��C2��	9��|d�%��V5=�)\J�*�k�2���Q���6�hL6 x	w��<=��><�������������]^R��g ��Ov@> �����[����_�����W�j�I�8����8H��n<5�f�g}}��3��\#�Ȕg���;$A*%6k;l�(Wj�HU�h:�@9{3̗xZ��7�ʡdz��pR�-��U6���tE�M�Z?Pr `�$��!nU�G:�}�-�kͦ��`�ͪ�4�&tfB�/).�BЂ����eb� ��$�L��#�dN(���CF:��z������5�$:� (��#-&��jEe�M@����Q��2ܥ��� f�s/��[gȖ���Y_�fa�u�/1�df�R����M�gk����F��f�4)C�tr���c�C�]�g3�	OSF4C���7n������"ի���0&��\��f�^S���Jͺ�U��X�o�xJ�0ۺ�H��%�Y�&[�[��d�U�<�#m�S��zܽ�ʮ���3��P|���븡�@8��k�M��m,� ��6����4�0��9#�6#��5�Ӏr�F�![n���F�f�.Q��0Pw�I�"��/>k�����:����Ɋ�:[5>�	�����څ9ʓ5y)�K+9�g.����������(m)�*F�1O����erj�+/|j�?U3���\�����`�v�U��p��,�p�X��`^���ZY�ݬ�h���?�~�Cg��!�a�/>.?6�^�Y7�jp
�L���\�>��#����5�����Ɲ�[�s�5���庌17o����Ym4kH��B�l�K&jy��b
'΅!��F�r��:�7:rj�iE@C��� B��|�y�Q��4"�	��4�M�E�`�<C+����Y��צ& f@Ply��[W��cO4����GW�����u�O����d�귏�"fB�+��z�۾HϺ�k�@���i�*O�>��T�v�xn�/�ӳ�F�,���4Z
�%��jKz6�f�BNM�Z�e	O=ħ�Y�0�wE�����3Ϝ��wIF��+����ja� &`�/躜K�0C���֎!ќ�c��\�z��ϛ�C��Y��h/��Y��n��m��Ө4����4�a��j@���+^���t��S��,������б~Hdv|��Sc�ƙ�8g���sb�0oŭ�	�K�q��������ݻ�p����q����E�1ϝ��O̼#<�����h��хW7+�f<+?1��zJ���ʂ�0^S��<����gK�D@�* kdr�DߥD��k1�IN���ޑ�FNɂD�c~�y)�.
8�;��=�<���}����AON�K�Ŕ��N��;���f{|t`� �i-�xA���}�̸yDna�:�h��?�VM�'� T�d�r~w9Έ���qҴ�}bl�����fc*�����Iӝ�]�;���d�IT6}K4���\r3���	�����ҧF�q��$hչ$oT���(T.}����o�G���4�DV��0e��*�^�#b�* �����[��I�:�j>:M�킎h��@�|?k�r�QAjA�9�7���������U2Bq.������TR �
#W���M��!��$z�|FCk
�P?��,e�4�M=?;M�_JTN�#j�c�>v����3�^5hn�~����-S�:��Wؾ���� ����]�jF����,���$<Y]��]A��Cn#QkC7�F��yZ���6`���}�(t�Ŀ0:P��<��>�3����E���dSˣ�v��C��rcalY����E0o?h�f_-W��m�D�m���48E�PTN�0�my�m	�`SuA40r$\y��.���)�E�L��1?���"����a9�FP�Ю=]�B+�0ꐏE~L�k�<c"-���閶<�n"�Sj1��PLl��1[$W���X��v���(X~ӏvL��D�4�ST����e&�~��I��Qo���(�.�#�Ba��5�YPqʧF8�P�2JpH(��Q����.��?-+�})�UqgE0`�#����p���~�h�)�fڠͥ  5L�W �unH'�@m�v|�,�N#o�1�y7�;2��B��+��H^�y�:�b�db�y��I�Ŭ+ ���X$���' nF���ĝ�cʚ�fa���7�����s��T��:]���RW ��[1=�oPL:���p����0ߘ����kSov�"*9��5�w�ǋR����5#��]�+�(`:���(���2�H�3�d"��Jr<����hu�¶	b��q��ӈ�((��ك����7Yf�%*���MgBm�"@ c�<��r�,�� ���?�wjn�X�!��I�!@q������{���{̔z�̘g<o�i!�y�$��4j�6�,�G��P(�}am>���p�Zb�Ȅ��6pы�$){�5�œ\���s�&d�-H�4�^_o>��@��Q�{J����'��8�+=���}��ru��Z1/+/�O�k��W�Ï�"P6ۨ=��k[۬���َ�T��o7.��}щ_إ��͎yn��lը7�jCR���� ���42��0P!3>�-i�+��嵜�'~�N$��$         �  x���mr�6DS��X`f����Ȁ�-m%�l�]Im�"�[� ��a4m���(G+�?�}��c���W�b�2�����J;Z��Q��}ԸL���a���ՏZ.����<���^?�8�y��W->��C�y��8z|��s�Gw��y�y6�1�������7\ŭ���G����.[�Z9�?���̭y�T�=���ّ�+O+��|�Svy@�ݎuD<�]��1g���9��O4�:������{�G���j/����6r8�t�s�������?�s��A��`�o�����|$g�}K=���t��w��9�^�˧��>�$y���ӷ�fp���r}�m~nzy�/����#�K���Vp3�~�D��u��L�	��;������U�a��q��{�[���}^87a�Zښ+q9�9
����O�W]�Zf�1[�7�>��Ž�����6�5k����~���̳��m�~�a��u�^7�˸��7g>�����k�M{Y}��Sʵܗr��Mz��9����ҟ�'u��sw^*�=A��}
��/�?�U�s~���є�<L��Õ������ѕ�<�ҟ�T��c	�9R����!��٤��� ���R�!��٥�<�ҟ�.��\J�L�P+WSz�2����h/�:9Z](Gk��]$G��#���ǫ��K�ɑ�Lʑ�"+�#/&�#/.�#��J&G^�N�<�N'G�O�:9�r䛣�#���#���ɑ�����/�#�� �#�Y&G^�R�<GP'G�'��#�I&G�[�N�<@Xs��r-o�t-�w�ȵ�u�kyN�ky^}ً\�Y�s-�%Y�kY�V��ҵ̄�e�t-�kYW���k�T�V�еr��u�*��t-7�k�K]k�ε�K]ˇе��H�k�R�V�е�*]+�ҵ¤����r�<2�kE׹V�k��V,�k�:$t�}\2��M�Z��+]��е�j	]k�V�V�.B��S�Z})]k��ε�c�k�&t�aJ��t���J�]�Z�z(]kL�k�%u�<&�k��"t�ٔ���%t��Rך�t�٥��_�\+�q�kͥ;�=�tG����WZ�2����2��]g��K-p�����D�,0JZ`������\g�QLh��_0�,0J�,0JZ`�����Sh�Q��#�Oh��Wf���\�F5�F�t�8d���c�d�Y`��2��kB�Vd�[�d�y�\+r0e�yG�\+�uR�ZѺε"oP�kE�2׊�r�\+rZ�\˪ҵ��\�L�Z�J��/�u�e]�Z6��eS�Z�R���k���t-oB�r����ҵrj]˻ҵ�;f�k���:9�"������P���������P�������������������]��#���Gta���ѕ=<�+{xD������]��#���G�ur4�=<bH�n�P�݈�l�Cٍ"��Ei7���n1��(b6������h�P�ra����J=�C�G����h.��1��(����ӣeJ=�%W�GiEB=Z]�GK�'���R���E�|k�����x}���<4_#�so���۹�W����\#M�c��<y�&;v��.���>5=v�\���Ŏ��;g��ǎ���z����wM�?�i����]�f7�׬MW��1�3dh��D=�!����.�s�<CZ��i�>69�vu�Z������'i=�|�tM뙘���O�z&�~��'RI�Ժ���uc��ޞ�\�͇��hk��YNڽ-Q���XU�ò���}��Q��tC�z���,
T�Y�ѳ,P�gQ�>Ϣ`u����<����i���<�B�y��4��i���0T��a�&O�PI����<��<MC�x��4tԦY��O�Pa����>Ce}���4�i%@5}K�4�}A�F�z� ��A4�h��,T
�a�D[,(�,P�Y�D�P���"�5 �K@4��i('�,T�ga�4E�`e�����u)��R4U�h*J�0T��a�$��p݇�����4�}��B�4dN�,9A�P��4�M�,7A�@��Ba4�}��BQ4$M�,4A�P�C14�L�,2A�P��4%L�00A�@�͂�4�K�0.A�P���4�*�I0�����
��>��F�P�PF�4%T�0P��*
��a0��ǁ�
�*x���
��t(�����
��*x
��i(�����
��*x��q(�����
*x��q(�����
�*x
��i(Q���D	�>Q�g�D	�%xH��a(Q���D	%xL��q Q���D	��>Q�g�D	�%xJ��i(Q���D	�%xJ��i(Q���D	J9<�@�8A�`O�J��!<�@�8��`�{��PO!<�@�0��@!<�@�8��PO{��PO!<�@�4��PO!<�@�4��`�C!<�@�8��`��!<�@�4��PO�!<�@�4��އ@�t-A�`O!<�@�0��@!<�@�8��PO{����i �����B x
��i �����B x��q(���B x��q(�����o���C x
��i0�Ɓ�U���P!<�@�4��@�!<�@�0A�@ϪJ�B!<�@�4��PO!<�@�4A?%�q|�U/��g3dw���6��F-fJ��
3%x̔�q0�ǡ��b x���i(��M�m�T	��S%x��SL��i�nU�J�0eǪ�R%x��kUé<Nع��T	���]�`�Ov�j0U��)�W5�*�ӄ�L��i�V8U��I�X�T	��c�#*x������i�^V0���I�Y5Q�Ӥ�����Y(�����
"*x���i �����
#*h���a(�������Y(�����
�"*x���i��Vm��
��pe8��>���ϱHم���O�G�Ժ��������#�Ի���[/����E��5^~�Um�����R�h�����n���{         ;  x��X]S�F}^~���x�,Y2O䋦S2��}�b��Y�d7�����)�0e���/�p�` a��z���!�0��JG�{���ɬ.��0��x���N����`u�_�#�!���a�f�DjrA3`3ˎ_�O
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
��t\���Ix�	ta�է�����`�t3'h�T�>���1I�7�͆���B��W�&����d�x��&���v#�����Ƥ��"~T��U���f�;u�;n�|uD���!�TpuV.k�,M��e5{��������j         �   x�3�LL��̃��FƜ&\�raυ�^�q��b�ņ.6]�w�A��B�Ѕ��\��,�hr(O,J��/-N�+*�4202�50�54T04�24�22�35�43��2��M�KLO-��`�� M��[.l��dɜ.l��`7l�L�)'ڢ=... �G[�         �  x��Wk��0�mN�d;1���P��J[	�j�UՖ�Vm��<�,,��7�g"Lȣ�d<��7�F����h�g:�X.h�OZ�^�����ہӮ�T�@O�F����U�fz��s�$�*�Q(�@�O*��^��I�V+r }�8�#Z���ziɊ62t�X�W�Y_y�\_p�%eCs��1î�k0����)�'<���o���г�9�c;����~ױg�π��0����z̊���&8���-q��f��=̮ !�s���+��7�-�D=��F��U&������;����{�큹�j�]�p����dȧ;_Ԁ��j C:0���P����V�_8�NOL���,����G�T��~e|a�7�A]F$�%>����byU5�Eh�=9U�+�R� �En��[�u�����-�7n��c���Y.�(a9Uy5h�[˾�������2F�ӁKӁ`Njr�(TdM��^���e"���u2��B溎����;K߫�d��c�.ʉ`z�5[v]]+wdnu����^qh��LΩ�S��EUw�!�b�9�aAS[�%q� ���s�o����D��%�%�hU�47 ҃���Ux�.�I�y�Hӭ�������ՙ�B��e��14��7�~�dB�Nu�!%�E�w��^<�״a'�:��F���I�1���S.���M���2_I���晗��-�u�š���Q2�e'ݾ�[/:�V�����     